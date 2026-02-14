"""
Telegram Notifier
Sends formatted alerts to Telegram
Uses direct requests API (matches proven p-signals implementation)
"""
import requests
import config
import json
from datetime import datetime

class TelegramNotifier:
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN if config.TELEGRAM_BOT_TOKEN else None
        self.chat_id = config.TELEGRAM_CHAT_ID if config.TELEGRAM_CHAT_ID else None
        self.sent_signals = set()  # Track sent signals to avoid duplicates
        self.load_sent_history()

    def load_sent_history(self):
        """Load previously sent signals"""
        try:
            with open('sent_signals.json', 'r') as f:
                data = json.load(f)
                self.sent_signals = set(data)
        except FileNotFoundError:
            pass

    def save_sent_history(self):
        """Save sent signals history"""
        with open('sent_signals.json', 'w') as f:
            json.dump(list(self.sent_signals), f)

    def send_signal_alert(self, signal):
        """Send Telegram alert for a detected signal"""
        if not self.bot_token or not self.chat_id:
            print(f"[TELEGRAM] Would send: {signal['pattern_name']}")
            return

        # Create unique ID for signal
        if signal['type'] == 'cluster':
            cluster = signal['cluster']
            signal_id = f"{cluster['market_id']}_{cluster['outcome']}_{cluster['num_wallets']}"
        else:
            signal_id = f"{signal['type']}_{datetime.now().isoformat()}"

        # Check if already sent
        if signal_id in self.sent_signals:
            return

        # Format message
        message = self.format_signal_message(signal)

        # Send using direct Telegram API (matches p-signals pattern)
        success = self._send_telegram(message)

        if success:
            # Track as sent
            self.sent_signals.add(signal_id)
            self.save_sent_history()
            print(f"✅ Sent alert: {signal['pattern_name']}")
        else:
            print(f"❌ Failed to send Telegram alert")

    def _send_telegram(self, message, parse_mode="HTML"):
        """Send message via direct Telegram API call (matches p-signals implementation)"""
        if not self.bot_token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }

        try:
            resp = requests.post(url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"Telegram error: {e}")
            return False

    def format_signal_message(self, signal):
        """Format signal data into Telegram message"""

        if signal['type'] == 'cluster':
            return self.format_cluster_signal(signal)
        elif signal['type'] == 'whale':
            return self.format_whale_signal(signal)
        elif signal['type'] == 'synchronized':
            return self.format_synchronized_signal(signal)
        else:
            return self.format_generic_signal(signal)

    def format_cluster_signal(self, signal):
        """Format high conviction cluster signal"""
        cluster = signal['cluster']
        conviction = signal['conviction']

        # Emoji based on conviction
        if conviction == "VERY HIGH":
            emoji = "🚨🚨🚨"
            position_pct = 10
        elif conviction == "HIGH":
            emoji = "🚨🚨"
            position_pct = 7
        else:
            emoji = "🚨"
            position_pct = 5

        # Calculate ROI
        price = cluster.get('price', 0.5)
        roi = (1 / price - 1) * 100 if price > 0 and price < 1 else 0

        # Get category
        category = cluster.get('category', 'Unknown')

        # Format wallet count (singular vs plural)
        num_wallets = cluster['num_wallets']
        wallet_text = f"{num_wallets} high-conviction wallet" if num_wallets == 1 else f"{num_wallets} high-conviction wallets"

        # Format market display
        question = cluster.get('question', 'Unknown')
        market_id = cluster.get('market_id', '')
        if question == 'Unknown' or question == 'UNKNOWN':
            # Show shortened token ID
            market_display = f"Token {market_id[:16]}..."
        else:
            market_display = question

        message = f"""
{emoji} <b>NEW {signal['pattern_name'].upper()}</b> {emoji}

<b>Pattern:</b> {signal['pattern_description']}

<b>Market:</b> {market_display}
<b>Outcome:</b> {cluster['outcome']}

💰 <b>Entry Price:</b> ${price:.3f} ({price*100:.1f}%)
📊 <b>Potential ROI:</b> +{roi:.0f}%
👥 <b>Wallets:</b> {wallet_text}
💵 <b>Total Volume:</b> ${cluster['total_volume']:,.0f}
🎯 <b>Conviction:</b> {cluster['avg_conviction']*100:.0f}%

<b>⏰ Timeline:</b>
• First Entry: {cluster['first_entry'].strftime('%m/%d %H:%M')}
• Latest Entry: {cluster['latest_entry'].strftime('%m/%d %H:%M')}

<b>📈 Recommended Position:</b> {position_pct}% of portfolio

<b>Category:</b> {category}
<b>🎯 Conviction: {conviction}</b>

<b>Historical Performance:</b>
"""

        # Add category-specific stats
        if category == 'Politics':
            message += "• Politics: 90% WR, 207% avg ROI\n"
        elif category == 'Financial':
            message += "• Financial: 100% WR, 3,471% avg ROI\n"

        # Add note if market name unknown
        if question == 'Unknown' or question == 'UNKNOWN':
            message += "\n<i>⚠️ Market name unavailable - check Polymarket for token details</i>\n"

        message += "\n<b>🎲 Check Polymarket/Kalshi for this market!</b>"

        return message

    def format_whale_signal(self, signal):
        """Format whale entry signal"""
        position = signal['position']

        # Calculate potential ROI based on entry price
        price = position.get('price', 0.5)
        roi = (1 / price - 1) * 100 if price > 0 and price < 1 else 0

        # Get category
        category = position.get('category', 'Unknown')

        # Format market display
        question = position.get('question', 'Unknown')
        market_id = position.get('market_id', '')
        if question == 'Unknown' or question == 'UNKNOWN':
            market_display = f"Token {market_id[:16]}..."
        else:
            market_display = question

        message = f"""
🐋 <b>WHALE ENTRY DETECTED</b>

<b>Pattern:</b> {signal['pattern_description']}

<b>Market:</b> {market_display}
<b>Outcome:</b> {position['outcome']}

💰 <b>Entry Price:</b> ${price:.3f} ({price*100:.1f}%)
📊 <b>Potential ROI:</b> +{roi:.0f}%

<b>Wallet:</b> {position['wallet'][:16]}...
<b>Position Size:</b> ${position['position_volume']:,.0f}
<b>Conviction:</b> {position['conviction']*100:.0f}%

<b>Category:</b> {category}

<i>Large wallet just entered with high conviction</i>

🎲 Check Polymarket/Kalshi for this market!
"""
        return message

    def format_synchronized_signal(self, signal):
        """Format synchronized entry signal"""
        cluster = signal['cluster']
        time_window = signal['time_window_hours']

        # Calculate ROI
        price = cluster.get('price', 0.5)
        roi = (1 / price - 1) * 100 if price > 0 and price < 1 else 0

        # Format market display
        question = cluster.get('question', 'Unknown')
        market_id = cluster.get('market_id', '')
        if question == 'Unknown' or question == 'UNKNOWN':
            market_display = f"Token {market_id[:16]}..."
        else:
            market_display = question

        message = f"""
⚡ <b>SYNCHRONIZED ENTRY</b>

<b>Pattern:</b> {signal['pattern_description']}

<b>{cluster['num_wallets']} wallets entered within {time_window:.1f} hours!</b>

<b>Market:</b> {market_display}
<b>Outcome:</b> {cluster['outcome']}

💰 <b>Entry Price:</b> ${price:.3f} ({price*100:.1f}%)
📊 <b>Potential ROI:</b> +{roi:.0f}%

<b>Total Volume:</b> ${cluster['total_volume']:,.0f}
<b>Conviction:</b> {cluster['avg_conviction']*100:.0f}%

<i>Coordinated entry suggests insider knowledge</i>

🎲 Check Kalshi for this market!
"""
        return message

    def format_generic_signal(self, signal):
        """Format generic signal"""
        return f"""
🚨 <b>{signal['pattern_name'].upper()}</b>

<b>Pattern:</b> {signal['pattern_description']}

<i>New signal detected - check details above</i>
"""

    def send_startup_message(self):
        """Send bot startup notification"""
        if not self.bot_token or not self.chat_id:
            return

        message = f"""
🤖 <b>Real-Time Scanner Started</b>

Monitoring Polygon blockchain for insider signals!

<b>Active Patterns:</b>
1. High Conviction Cluster (5+ wallets, $2K+, 85%+ conviction)
2. Whale Entry ($10K+ single wallet)
3. Synchronized Entry (coordinated timing)

<b>Tracking:</b>
• Politics (90% WR, 223% ROI)
• Financial (100% WR, 3,471% ROI)

<b>Thresholds:</b>
• Min Volume: ${config.MIN_WALLET_VOLUME}
• Min Conviction: {int(config.MIN_CONVICTION*100)}%
• Min Wallets: {config.MIN_WALLETS_CLUSTER}+

<b>Scan Interval:</b> Every {config.SCAN_INTERVAL_SECONDS//60} minutes

Ready to detect signals! 🚀
"""

        success = self._send_telegram(message)
        if not success:
            print(f"Failed to send startup message")

    def send_daily_summary(self, stats):
        """Send daily summary of detected signals"""
        if not self.bot_token or not self.chat_id:
            return

        message = f"""
📊 <b>Daily Scanner Summary</b>

<b>Signals Detected:</b> {stats.get('signals_detected', 0)}
<b>Blocks Scanned:</b> {stats.get('blocks_scanned', 0):,}
<b>Trades Processed:</b> {stats.get('trades_processed', 0):,}
<b>Wallets Tracked:</b> {stats.get('wallets_tracked', 0):,}

<b>Status:</b> ✅ Running
"""

        success = self._send_telegram(message)
        if not success:
            print(f"Failed to send summary")

    def test_connection(self):
        """Test Telegram connection (matches p-signals pattern)"""
        message = "🟢 <b>Polymarket Scanner Connected!</b>\n\nYou will receive insider trading signals here."
        success = self._send_telegram(message)
        if success:
            print("✅ Telegram test successful!")
            return True
        else:
            print("❌ Telegram test failed!")
            return False
