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
        """Parse trade data from transaction log"""
        try:
            # This is simplified - real implementation would decode ABI
            # For Polymarket CTF Exchange, we'd decode:
            # - maker/taker addresses
            # - token IDs (which encode market + outcome)
            # - amounts
            # - price

            # Placeholder structure
            return {
                'wallet': log.get('address', '0x0'),
                'market_id': 'unknown',
                'outcome': 'unknown',
                'volume_usd': 0,
                'price': 0,
                'timestamp': datetime.now(),
                'block_number': log.get('blockNumber', 0),
                'tx_hash': log.get('transactionHash', '0x0')
            }
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
                trade = self.parse_trade_from_log(log)
                if trade:
                    trades.append(trade)

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

            # Enrich trades
            for trade in trades:
                if trade['market_id'] in markets_lookup:
                    market = markets_lookup[trade['market_id']]
                    trade['question'] = market.get('question', 'Unknown')
                    trade['category'] = self.categorize_market(market.get('question', ''))
                    trade['tokens'] = market.get('tokens', [])

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
