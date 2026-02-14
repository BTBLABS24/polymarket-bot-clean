#!/usr/bin/env python3
"""
Test Telegram Bot Connection
Tests if bot token and chat ID are working correctly
"""
import sys
import os

# Add realtime_scanner to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'realtime_scanner'))

from telegram_notifier import TelegramNotifier
import config

def main():
    print("="*60)
    print("TELEGRAM BOT CONNECTION TEST")
    print("="*60)
    print()

    # Check config
    print("1. Checking configuration...")
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        print("   Set it in realtime_scanner/config.py or as environment variable")
        return False

    if not config.TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_CHAT_ID not set!")
        print("   Set it in realtime_scanner/config.py or as environment variable")
        return False

    print(f"✅ Bot Token: {config.TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"✅ Chat ID: {config.TELEGRAM_CHAT_ID}")
    print()

    # Test connection
    print("2. Testing Telegram connection...")
    notifier = TelegramNotifier()
    success = notifier.test_connection()
    print()

    if success:
        print("="*60)
        print("✅ SUCCESS! Telegram bot is working!")
        print("="*60)
        print()
        print("Next steps:")
        print("1. Deploy scanner to Railway (see DEPLOYMENT.md)")
        print("2. Scanner will send signals as they're detected")
        return True
    else:
        print("="*60)
        print("❌ FAILED! Telegram bot not working")
        print("="*60)
        print()
        print("Troubleshooting:")
        print("1. Verify bot token is correct")
        print("2. Verify you started chat with bot (@YourBotName)")
        print("3. Verify chat ID is correct (use /start with bot)")
        print()
        print("See TELEGRAM_BOT_TROUBLESHOOTING.md for detailed help")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
