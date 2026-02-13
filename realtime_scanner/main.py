#!/usr/bin/env python3
"""
Real-Time Polymarket Scanner
Monitors blockchain, detects wallet patterns, sends Telegram alerts
"""
import asyncio
import time
from datetime import datetime
import config
from wallet_tracker import WalletTracker
from blockchain_scanner import BlockchainScanner
from signal_detector import SignalDetector
from telegram_notifier import TelegramNotifier

class RealtimeScanner:
    def __init__(self):
        self.wallet_tracker = WalletTracker()
        self.blockchain_scanner = BlockchainScanner()
        self.signal_detector = SignalDetector()
        self.telegram_notifier = TelegramNotifier()

        # Stats
        self.stats = {
            'signals_detected': 0,
            'blocks_scanned': 0,
            'trades_processed': 0,
            'wallets_tracked': 0,
            'last_scan': None
        }

        # Load saved state
        self.wallet_tracker.load_state()

    async def scan_cycle(self):
        """Single scan cycle"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting scan cycle...")
        print(f"{'='*60}")

        try:
            # 1. Get current block
            latest_block = self.blockchain_scanner.get_latest_block()
            last_processed = self.blockchain_scanner.load_checkpoint()

            print(f"Latest block: {latest_block}")
            print(f"Last processed: {last_processed}")
            print(f"Blocks to process: {latest_block - last_processed}")

            # 2. Process new blocks in batches
            current = last_processed + 1
            trades_this_cycle = []

            while current <= latest_block:
                to_block = min(current + config.BLOCK_BATCH_SIZE, latest_block)

                print(f"Processing blocks {current} to {to_block}...")

                # Get trades from this batch
                trades = self.blockchain_scanner.get_recent_trades(current, to_block)
                trades_this_cycle.extend(trades)

                # Update stats
                self.stats['blocks_scanned'] += (to_block - current + 1)
                self.stats['trades_processed'] += len(trades)

                current = to_block + 1

            print(f"✅ Found {len(trades_this_cycle)} trades in this cycle")

            # 3. Enrich trades with market data
            if trades_this_cycle:
                trades_this_cycle = self.blockchain_scanner.enrich_with_polymarket_data(trades_this_cycle)

            # 4. Update wallet tracker
            for trade in trades_this_cycle:
                self.wallet_tracker.add_trade(
                    wallet=trade['wallet'],
                    market_id=trade['market_id'],
                    outcome=trade['outcome'],
                    volume_usd=trade['volume_usd'],
                    timestamp=trade['timestamp']
                )

            # 5. Detect clusters
            clusters = self.wallet_tracker.detect_clusters(
                min_wallets=config.MIN_WALLETS_CLUSTER,
                min_volume=config.MIN_WALLET_VOLUME,
                min_conviction=config.MIN_CONVICTION
            )

            print(f"✅ Detected {len(clusters)} wallet clusters")

            # 6. Run signal detection patterns
            signals = self.signal_detector.detect_all(
                clusters,
                trades_this_cycle,
                self.wallet_tracker
            )

            print(f"🚨 Found {len(signals)} signals!")

            # 7. Send Telegram alerts
            for signal in signals:
                await self.telegram_notifier.send_signal_alert(signal)
                self.stats['signals_detected'] += 1

            # 8. Save state
            self.blockchain_scanner.save_checkpoint(latest_block)
            self.wallet_tracker.save_state()

            # 9. Cleanup old data
            self.wallet_tracker.cleanup_old_data(hours=config.LOOKBACK_HOURS)

            # Update stats
            self.stats['wallets_tracked'] = len(self.wallet_tracker.wallet_totals)
            self.stats['last_scan'] = datetime.now()

            print(f"✅ Scan cycle complete")
            print(f"   Wallets tracked: {self.stats['wallets_tracked']}")
            print(f"   Signals detected (total): {self.stats['signals_detected']}")

        except Exception as e:
            print(f"❌ Error in scan cycle: {e}")
            import traceback
            traceback.print_exc()

    async def run(self):
        """Main scanner loop"""

        # Send startup message
        await self.telegram_notifier.send_startup_message()

        print("="*60)
        print("REAL-TIME POLYMARKET SCANNER")
        print("="*60)
        print(f"Alchemy API: {'✅ Connected' if config.ALCHEMY_API_KEY else '❌ Not configured'}")
        print(f"Telegram: {'✅ Connected' if config.TELEGRAM_BOT_TOKEN else '❌ Not configured'}")
        print(f"Scan interval: Every {config.SCAN_INTERVAL_SECONDS} seconds")
        print(f"Min wallet volume: ${config.MIN_WALLET_VOLUME}")
        print(f"Min conviction: {config.MIN_CONVICTION*100}%")
        print(f"Min wallets for signal: {config.MIN_WALLETS_CLUSTER}")
        print("="*60)
        print()

        last_daily_summary = datetime.now()

        # Main loop
        while True:
            try:
                # Run scan cycle
                await self.scan_cycle()

                # Send daily summary
                hours_since_summary = (datetime.now() - last_daily_summary).total_seconds() / 3600
                if hours_since_summary >= 24:
                    await self.telegram_notifier.send_daily_summary(self.stats)
                    last_daily_summary = datetime.now()

                # Wait for next cycle
                print(f"\n⏰ Next scan in {config.SCAN_INTERVAL_SECONDS} seconds...\n")
                await asyncio.sleep(config.SCAN_INTERVAL_SECONDS)

            except KeyboardInterrupt:
                print("\n👋 Scanner stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                import traceback
                traceback.print_exc()
                # Wait before retrying
                await asyncio.sleep(60)

if __name__ == "__main__":
    scanner = RealtimeScanner()

    try:
        asyncio.run(scanner.run())
    except KeyboardInterrupt:
        print("\n👋 Scanner stopped")
