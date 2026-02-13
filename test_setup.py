#!/usr/bin/env python3
"""
Quick test to verify scanner setup
"""
import sys
import os

# Add realtime_scanner to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'realtime_scanner'))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")

    try:
        import config
        print("✅ config.py imported")
    except Exception as e:
        print(f"❌ config.py failed: {e}")
        return False

    try:
        from wallet_tracker import WalletTracker
        print("✅ wallet_tracker.py imported")
    except Exception as e:
        print(f"❌ wallet_tracker.py failed: {e}")
        return False

    try:
        from blockchain_scanner import BlockchainScanner
        print("✅ blockchain_scanner.py imported")
    except Exception as e:
        print(f"❌ blockchain_scanner.py failed: {e}")
        return False

    try:
        from signal_detector import SignalDetector
        print("✅ signal_detector.py imported")
    except Exception as e:
        print(f"❌ signal_detector.py failed: {e}")
        return False

    try:
        from telegram_notifier import TelegramNotifier
        print("✅ telegram_notifier.py imported")
    except Exception as e:
        print(f"❌ telegram_notifier.py failed: {e}")
        return False

    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    import config

    print(f"Alchemy API Key: {'✅ Set' if config.ALCHEMY_API_KEY else '❌ Not set'}")
    print(f"Telegram Bot Token: {'✅ Set' if config.TELEGRAM_BOT_TOKEN else '❌ Not set'}")
    print(f"Telegram Chat ID: {'✅ Set' if config.TELEGRAM_CHAT_ID else '❌ Not set'}")
    print(f"Min Wallet Volume: ${config.MIN_WALLET_VOLUME}")
    print(f"Min Conviction: {config.MIN_CONVICTION*100}%")
    print(f"Min Wallets for Cluster: {config.MIN_WALLETS_CLUSTER}")
    print(f"Scan Interval: {config.SCAN_INTERVAL_SECONDS}s")

def test_classes():
    """Test if classes can be instantiated"""
    print("\nTesting class instantiation...")

    try:
        from wallet_tracker import WalletTracker
        tracker = WalletTracker()
        print("✅ WalletTracker instantiated")
    except Exception as e:
        print(f"❌ WalletTracker failed: {e}")
        return False

    try:
        from blockchain_scanner import BlockchainScanner
        scanner = BlockchainScanner()
        print("✅ BlockchainScanner instantiated")
    except Exception as e:
        print(f"❌ BlockchainScanner failed: {e}")
        return False

    try:
        from signal_detector import SignalDetector
        detector = SignalDetector()
        print(f"✅ SignalDetector instantiated with {len(detector.patterns)} patterns")
    except Exception as e:
        print(f"❌ SignalDetector failed: {e}")
        return False

    try:
        from telegram_notifier import TelegramNotifier
        notifier = TelegramNotifier()
        print("✅ TelegramNotifier instantiated")
    except Exception as e:
        print(f"❌ TelegramNotifier failed: {e}")
        return False

    return True

if __name__ == "__main__":
    print("="*60)
    print("POLYMARKET SCANNER SETUP TEST")
    print("="*60)

    success = True

    if not test_imports():
        success = False

    test_config()

    if not test_classes():
        success = False

    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED - Scanner is ready!")
        print("="*60)
        print("\nNext steps:")
        print("1. Set ALCHEMY_API_KEY environment variable")
        print("2. Run: cd realtime_scanner && python main.py")
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
        print("="*60)
