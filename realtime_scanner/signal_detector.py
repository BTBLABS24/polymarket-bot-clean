"""
Signal Detector - Modular Pattern Detection
Easy to add new signal patterns
"""
import config
from datetime import datetime

class SignalDetector:
    def __init__(self):
        self.patterns = []
        self.register_default_patterns()

    def register_pattern(self, pattern_func, name, description):
        """Register a new signal detection pattern"""
        self.patterns.append({
            'func': pattern_func,
            'name': name,
            'description': description
        })

    def register_default_patterns(self):
        """Register default patterns"""

        # Pattern 1: High Conviction Signal (your main pattern)
        self.register_pattern(
            self.pattern_high_conviction_cluster,
            "High Conviction Signal",
            "Wallet(s) with $1K+ volume, 80%+ conviction on same outcome"
        )

        # Pattern 2: Whale Entry (single large wallet)
        self.register_pattern(
            self.pattern_whale_entry,
            "Whale Entry",
            "Single wallet $10K+ with 80%+ conviction"
        )

        # Pattern 3: Synchronized Entry (wallets enter at same time)
        self.register_pattern(
            self.pattern_synchronized_entry,
            "Synchronized Entry",
            "5+ wallets enter within 1 hour window"
        )

    def detect_all(self, clusters, trades, wallet_tracker):
        """Run all pattern detections"""
        signals = []

        for pattern in self.patterns:
            detected = pattern['func'](clusters, trades, wallet_tracker)
            if detected:
                for signal in detected:
                    signal['pattern_name'] = pattern['name']
                    signal['pattern_description'] = pattern['description']
                signals.extend(detected)

        return signals

    # ========== PATTERN FUNCTIONS ==========

    def pattern_high_conviction_cluster(self, clusters, trades, wallet_tracker):
        """
        Pattern 1: High Conviction Signal
        YOUR MAIN PATTERN - ANY wallet(s) with $1K+, 80%+ conviction
        """
        signals = []

        for cluster in clusters:
            # Filter by category
            if 'category' not in cluster or cluster['category'] not in ['Politics', 'Financial']:
                continue

            # Filter by price
            if 'price' in cluster and cluster['price'] > config.MAX_PRICE:
                continue

            # Calculate conviction score based on wallets, volume, and price
            num_wallets = cluster['num_wallets']
            price = cluster.get('price', 1)
            total_volume = cluster['total_volume']
            avg_conviction = cluster['avg_conviction']

            # Score based on multiple factors
            if num_wallets >= 20 and price < 0.30:
                conviction_score = "VERY HIGH"
            elif num_wallets >= 10 and price < 0.40:
                conviction_score = "VERY HIGH"
            elif num_wallets >= 5 and price < 0.50:
                conviction_score = "HIGH"
            elif num_wallets >= 3 and avg_conviction >= 0.90:
                conviction_score = "HIGH"
            elif num_wallets >= 2 and total_volume >= 5000:
                conviction_score = "MEDIUM"
            elif num_wallets == 1 and total_volume >= 5000 and avg_conviction >= 0.90:
                conviction_score = "MEDIUM"
            else:
                conviction_score = "LOW"

            signals.append({
                'type': 'cluster',
                'conviction': conviction_score,
                'cluster': cluster
            })

        return signals

    def pattern_whale_entry(self, clusters, trades, wallet_tracker):
        """
        Pattern 2: Whale Entry
        Single large wallet ($10K+) with high conviction
        """
        signals = []

        high_conviction = wallet_tracker.get_high_conviction_wallets(
            min_volume=10000,
            min_conviction=0.80
        )

        for position in high_conviction:
            # Check if this is a new entry (within last hour)
            time_since_entry = (datetime.now() - position['timestamp']).total_seconds() / 3600

            if time_since_entry <= 1:  # Last hour
                signals.append({
                    'type': 'whale',
                    'conviction': 'HIGH',
                    'position': position
                })

        return signals

    def pattern_synchronized_entry(self, clusters, trades, wallet_tracker):
        """
        Pattern 3: Synchronized Entry
        Multiple wallets entering within short time window
        """
        signals = []

        for cluster in clusters:
            if cluster['num_wallets'] < 5:
                continue

            # Check if entries are synchronized (within 1 hour)
            time_window = (cluster['latest_entry'] - cluster['first_entry']).total_seconds() / 3600

            if time_window <= 1:  # All entered within 1 hour
                signals.append({
                    'type': 'synchronized',
                    'conviction': 'HIGH',
                    'cluster': cluster,
                    'time_window_hours': time_window
                })

        return signals

    # ========== ADD YOUR OWN PATTERNS HERE ==========

    def pattern_velocity_scaling(self, clusters, trades, wallet_tracker):
        """
        Pattern 4: Velocity Scaling (PLACEHOLDER - Add your logic)
        Wallets progressively increasing position size
        """
        # TODO: Implement velocity scaling detection
        return []

    def pattern_layering(self, clusters, trades, wallet_tracker):
        """
        Pattern 5: Layering (PLACEHOLDER - Add your logic)
        Multiple entries at different price levels
        """
        # TODO: Implement layering detection
        return []
