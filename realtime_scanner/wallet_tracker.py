"""
Wallet Activity Tracker
Monitors wallets and calculates conviction levels
"""
from collections import defaultdict
from datetime import datetime, timedelta
import json

class WalletTracker:
    def __init__(self):
        # wallet_address -> {market_id -> {outcome -> volume}}
        self.wallet_positions = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        # wallet_address -> total_volume
        self.wallet_totals = defaultdict(float)

        # market_id -> {outcome -> [wallet_addresses]}
        self.market_clusters = defaultdict(lambda: defaultdict(set))

        # Track when positions were entered
        self.position_timestamps = {}

    def add_trade(self, wallet, market_id, outcome, volume_usd, timestamp=None):
        """Add a trade to tracker"""
        if timestamp is None:
            timestamp = datetime.now()

        # Update wallet position
        self.wallet_positions[wallet][market_id][outcome] += volume_usd
        self.wallet_totals[wallet] += volume_usd

        # Track timestamp
        key = (wallet, market_id, outcome)
        if key not in self.position_timestamps:
            self.position_timestamps[key] = timestamp

    def get_wallet_conviction(self, wallet, market_id, outcome):
        """Calculate wallet's conviction on specific position"""
        position_volume = self.wallet_positions[wallet][market_id][outcome]
        total_volume = self.wallet_totals[wallet]

        if total_volume == 0:
            return 0

        return position_volume / total_volume

    def get_high_conviction_wallets(self, min_volume=1000, min_conviction=0.80):
        """Find wallets with high conviction (80%+ on single position)"""
        high_conviction = []

        for wallet, total_volume in self.wallet_totals.items():
            if total_volume < min_volume:
                continue

            # Check each position for this wallet
            for market_id, outcomes in self.wallet_positions[wallet].items():
                for outcome, position_volume in outcomes.items():
                    conviction = position_volume / total_volume

                    if conviction >= min_conviction:
                        high_conviction.append({
                            'wallet': wallet,
                            'market_id': market_id,
                            'outcome': outcome,
                            'position_volume': position_volume,
                            'total_volume': total_volume,
                            'conviction': conviction,
                            'timestamp': self.position_timestamps.get(
                                (wallet, market_id, outcome),
                                datetime.now()
                            )
                        })

        return high_conviction

    def detect_clusters(self, min_wallets=5, min_volume=1000, min_conviction=0.80):
        """Find clusters of high-conviction wallets on same market"""
        # Get all high conviction wallets
        high_conviction = self.get_high_conviction_wallets(min_volume, min_conviction)

        # Group by market and outcome
        clusters = defaultdict(list)
        for position in high_conviction:
            key = (position['market_id'], position['outcome'])
            clusters[key].append(position)

        # Filter to clusters with min_wallets+
        signals = []
        for (market_id, outcome), wallets in clusters.items():
            if len(wallets) >= min_wallets:
                signals.append({
                    'market_id': market_id,
                    'outcome': outcome,
                    'num_wallets': len(wallets),
                    'wallets': wallets,
                    'total_volume': sum(w['position_volume'] for w in wallets),
                    'avg_conviction': sum(w['conviction'] for w in wallets) / len(wallets),
                    'first_entry': min(w['timestamp'] for w in wallets),
                    'latest_entry': max(w['timestamp'] for w in wallets)
                })

        return signals

    def cleanup_old_data(self, hours=72):
        """Remove positions older than X hours"""
        cutoff = datetime.now() - timedelta(hours=hours)

        old_keys = [
            key for key, timestamp in self.position_timestamps.items()
            if timestamp < cutoff
        ]

        for wallet, market_id, outcome in old_keys:
            volume = self.wallet_positions[wallet][market_id][outcome]

            # Remove from tracking
            del self.wallet_positions[wallet][market_id][outcome]
            self.wallet_totals[wallet] -= volume
            del self.position_timestamps[(wallet, market_id, outcome)]

            # Clean empty dicts
            if not self.wallet_positions[wallet][market_id]:
                del self.wallet_positions[wallet][market_id]
            if not self.wallet_positions[wallet]:
                del self.wallet_positions[wallet]
                del self.wallet_totals[wallet]

    def save_state(self, filename='wallet_tracker_state.json'):
        """Save tracker state to file"""
        state = {
            'wallet_positions': {
                w: {m: dict(o) for m, o in markets.items()}
                for w, markets in self.wallet_positions.items()
            },
            'wallet_totals': dict(self.wallet_totals),
            'position_timestamps': {
                f"{k[0]}_{k[1]}_{k[2]}": v.isoformat()
                for k, v in self.position_timestamps.items()
            }
        }

        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, filename='wallet_tracker_state.json'):
        """Load tracker state from file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)

            # Restore wallet positions
            for wallet, markets in state['wallet_positions'].items():
                for market_id, outcomes in markets.items():
                    for outcome, volume in outcomes.items():
                        self.wallet_positions[wallet][market_id][outcome] = volume

            # Restore totals
            self.wallet_totals = defaultdict(float, state['wallet_totals'])

            # Restore timestamps
            for key_str, timestamp_str in state['position_timestamps'].items():
                wallet, market_id, outcome = key_str.split('_', 2)
                key = (wallet, market_id, outcome)
                self.position_timestamps[key] = datetime.fromisoformat(timestamp_str)

            return True
        except FileNotFoundError:
            return False
