"""
Blockchain Scanner
Connects to Polygon via Alchemy and monitors Polymarket trades
"""
from web3 import Web3
import requests
from datetime import datetime
import time
import config

class BlockchainScanner:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.POLYGON_RPC))

        # Add POA middleware for Polygon
        try:
            from web3.middleware import ExtraDataToPOAMiddleware
            self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        except:
            pass  # Middleware not needed or already injected

        self.current_block = None
        self.market_cache = {}  # market_id -> {question, tokens, etc}

    def get_latest_block(self):
        """Get latest block number"""
        return self.w3.eth.block_number

    def get_market_info(self, market_id):
        """Get market information from Polymarket API"""
        if market_id in self.market_cache:
            return self.market_cache[market_id]

        try:
            # Try to find market info
            # This would query Polymarket's API or indexer
            # For now, return placeholder
            return {
                'question': f'Market {market_id[:8]}...',
                'tokens': [],
                'category': 'Unknown'
            }
        except:
            return None

    def parse_trade_from_log(self, log):
        """
        Parse trade data from OrderFilled event log

        Event structure:
        - topics[0] = event signature
        - topics[1] = orderHash (indexed)
        - topics[2] = maker address (indexed, 32 bytes padded)
        - topics[3] = taker address (indexed, 32 bytes padded)
        - data = [makerAssetId, takerAssetId, makerAmountFilled, takerAmountFilled, fee]
        """
        try:
            topics = log.get('topics', [])
            raw_data = log.get('data', '0x')

            # Convert data to hex string if it's bytes
            if isinstance(raw_data, bytes):
                data = raw_data.hex()
            elif isinstance(raw_data, str):
                data = raw_data[2:] if raw_data.startswith('0x') else raw_data
            else:
                return None

            # Need at least 4 topics and data (5 uint256 = 160 bytes = 320 hex chars)
            # But sometimes data is 158 bytes, so let's be flexible
            if len(topics) < 4 or len(data) < 300:
                return None

            # Extract maker and taker addresses from topics
            # Topics are 32 bytes, addresses are last 20 bytes
            def extract_address(topic):
                if isinstance(topic, bytes):
                    # Already bytes, take last 20 bytes
                    return '0x' + topic[-20:].hex().lower()
                elif hasattr(topic, 'hex'):
                    # HexBytes object
                    return '0x' + topic.hex()[26:].lower()
                elif isinstance(topic, str):
                    # Hex string
                    hex_str = topic[2:] if topic.startswith('0x') else topic
                    return '0x' + hex_str[24:].lower()
                return '0x0'

            maker = extract_address(topics[2])
            taker = extract_address(topics[3])

            # Extract data fields (each is 64 hex chars = 32 bytes)
            maker_asset_id = int(data[0:64], 16)
            taker_asset_id = int(data[64:128], 16)
            maker_amount = int(data[128:192], 16)
            taker_amount = int(data[192:256], 16)
            fee = int(data[256:320], 16)

            # Convert amounts from USDC (6 decimals)
            maker_volume_usd = maker_amount / 1e6
            taker_volume_usd = taker_amount / 1e6

            # Calculate price (simplified)
            price = (taker_amount / maker_amount) if maker_amount > 0 else 0

            block_num = log.get('blockNumber', 0)
            tx_hash = log.get('transactionHash', '0x0')
            if hasattr(tx_hash, 'hex'):
                tx_hash = tx_hash.hex()

            # Return TWO trades: one for maker, one for taker
            return [
                {
                    'wallet': maker,
                    'market_id': str(maker_asset_id),
                    'outcome': 'YES',  # Simplified - would need token mapping
                    'volume_usd': maker_volume_usd,
                    'price': price,
                    'timestamp': datetime.now(),
                    'block_number': block_num,
                    'tx_hash': str(tx_hash),
                    'side': 'maker'
                },
                {
                    'wallet': taker,
                    'market_id': str(taker_asset_id),
                    'outcome': 'YES',  # Simplified - would need token mapping
                    'volume_usd': taker_volume_usd,
                    'price': 1 - price if price > 0 else 0,
                    'timestamp': datetime.now(),
                    'block_number': block_num,
                    'tx_hash': str(tx_hash),
                    'side': 'taker'
                }
            ]
        except Exception as e:
            print(f"Error parsing log: {e}")
            return None

    def get_recent_trades(self, from_block, to_block):
        """Get trades from block range"""
        trades = []

        try:
            # Get logs from CTF Exchange contract
            logs = self.w3.eth.get_logs({
                'address': config.CTF_EXCHANGE,
                'fromBlock': from_block,
                'toBlock': to_block
            })

            for log in logs:
                parsed = self.parse_trade_from_log(log)
                if parsed:
                    # parse_trade_from_log returns a list of trades (maker + taker)
                    if isinstance(parsed, list):
                        trades.extend(parsed)
                    else:
                        trades.append(parsed)

        except Exception as e:
            print(f"Error fetching logs: {e}")

        return trades

    def enrich_with_polymarket_data(self, trades):
        """Add market metadata to trades"""
        # Get unique market IDs
        market_ids = set(t['market_id'] for t in trades if t['market_id'] != 'unknown')

        # Fetch market data from Polymarket API
        try:
            response = requests.get('https://gamma-api.polymarket.com/markets', timeout=10)
            markets_data = response.json()

            # Build lookup
            markets_lookup = {m.get('conditionId'): m for m in markets_data}

            # Enrich trades and cache market data
            for trade in trades:
                if trade['market_id'] in markets_lookup:
                    market = markets_lookup[trade['market_id']]
                    trade['question'] = market.get('question', 'Unknown')
                    trade['category'] = self.categorize_market(market.get('question', ''))
                    trade['tokens'] = market.get('tokens', [])

                    # Cache market data for later lookups
                    self.market_cache[trade['market_id']] = {
                        'question': trade['question'],
                        'category': trade['category'],
                        'tokens': trade['tokens']
                    }

        except Exception as e:
            print(f"Error enriching trades: {e}")

        return trades

    def categorize_market(self, question):
        """Categorize market based on question"""
        question_lower = question.lower()

        # Check Politics
        if any(kw in question_lower for kw in config.POLITICS_KEYWORDS):
            if not any(kw in question_lower for kw in config.EXCLUDE_KEYWORDS):
                return 'Politics'

        # Check Financial
        if any(kw in question_lower for kw in config.FINANCIAL_KEYWORDS):
            return 'Financial'

        # Check exclusions
        if any(kw in question_lower for kw in config.EXCLUDE_KEYWORDS):
            return 'Excluded'

        return 'Other'

    def save_checkpoint(self, block_number):
        """Save current block checkpoint"""
        with open('scanner_checkpoint.txt', 'w') as f:
            f.write(str(block_number))

    def load_checkpoint(self):
        """Load last processed block"""
        try:
            with open('scanner_checkpoint.txt', 'r') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            # Start from recent block if no checkpoint
            return self.get_latest_block() - 1000
