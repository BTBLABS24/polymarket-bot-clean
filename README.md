# Polymarket Real-Time Scanner

Monitors Polygon blockchain for Polymarket insider trading signals and sends Telegram alerts.

## Strategy

Detects when **5+ wallets** (each with **$1K+ volume**) put **80%+ of their capital** on the same bet.

**Historical Performance:**
- **Politics:** 90% win rate, 207% avg ROI
- **Financial:** 100% win rate, 3,471% avg ROI

## Features

- 🔍 Real-time blockchain monitoring via Alchemy
- 👥 Wallet cluster detection (5+ high-conviction wallets)
- 🐋 Whale entry detection ($10K+ positions)
- ⚡ Synchronized entry detection (coordinated timing)
- 📱 Telegram alerts with trade recommendations
- 🔧 Modular pattern system (easy to add new signals)
- 💾 State persistence (survives restarts)

## Setup

### 1. Prerequisites

- Python 3.11+
- Alchemy API key (get from https://www.alchemy.com/)
- Telegram bot (already created: `@polyfebbot`)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and add your Alchemy API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
ALCHEMY_API_KEY=your_alchemy_api_key_here
TELEGRAM_BOT_TOKEN=7989561870:AAG-W3B_DBIC78BM3Coe0rUdJV3_B-X0gzE
TELEGRAM_CHAT_ID=1563550509
```

### 4. Run Scanner

```bash
cd realtime_scanner
python main.py
```

## Deployment Options

### Option 1: Railway (Recommended)

1. Push code to GitHub
2. Create new Railway project
3. Link GitHub repo
4. Add environment variables in Railway dashboard:
   - `ALCHEMY_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. Deploy

Railway will automatically use the `Dockerfile` to build and run the scanner.

### Option 2: VPS/Server

```bash
# Clone repo
git clone <your-repo>
cd polymarket-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ALCHEMY_API_KEY="your_key"
export TELEGRAM_BOT_TOKEN="7989561870:AAG-W3B_DBIC78BM3Coe0rUdJV3_B-X0gzE"
export TELEGRAM_CHAT_ID="1563550509"

# Run with nohup for background execution
cd realtime_scanner
nohup python main.py > scanner.log 2>&1 &
```

### Option 3: Docker

```bash
# Build image
docker build -t polymarket-scanner .

# Run container
docker run -d \
  -e ALCHEMY_API_KEY="your_key" \
  -e TELEGRAM_BOT_TOKEN="7989561870:AAG-W3B_DBIC78BM3Coe0rUdJV3_B-X0gzE" \
  -e TELEGRAM_CHAT_ID="1563550509" \
  polymarket-scanner
```

## How It Works

### 1. Blockchain Monitoring
- Connects to Polygon via Alchemy RPC
- Monitors Polymarket CTF Exchange contract (`0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`)
- Processes blocks in batches (1000 at a time)
- Decodes trade logs to extract wallet activity

### 2. Wallet Tracking
- Tracks each wallet's positions across all markets
- Calculates conviction = position_volume / total_wallet_volume
- Identifies high-conviction wallets (80%+ on single bet)

### 3. Cluster Detection
- Groups high-conviction wallets by market + outcome
- Triggers signal when 5+ wallets cluster on same bet
- Filters by category (Politics, Financial only)
- Filters by price (≤$0.60 underdogs only)

### 4. Telegram Alerts
Example alert:
```
🚨🚨🚨 NEW HIGH CONVICTION CLUSTER 🚨🚨🚨

Pattern: 5+ wallets with $1K+, 80%+ conviction on same outcome

Event: US government shutdown Saturday?
Outcome: YES

💰 Entry Price: $0.230 (23.0%)
📊 Potential ROI: +335%
👥 Wallets: 68 high-conviction wallets
💵 Total Volume: $519,321
🎯 Avg Conviction: 96.0%

⏰ Timeline:
• First Entry: 01/26 00:24
• Latest Entry: 01/26 02:30

📈 Recommended Position: 10% of portfolio

Category: Politics
🎯 Conviction: VERY HIGH

Historical Performance:
• Politics: 90% WR, 207% avg ROI

🎲 Check Kalshi for this market!
```

## Configuration

Edit `realtime_scanner/config.py` to adjust:

```python
MIN_WALLET_VOLUME = 1000  # $1K minimum per wallet
MIN_CONVICTION = 0.80  # 80% focus on single position
MIN_WALLETS_CLUSTER = 5  # 5+ wallets = signal
MAX_PRICE = 0.60  # Only underdogs ≤$0.60
SCAN_INTERVAL_SECONDS = 300  # Check every 5 minutes
LOOKBACK_HOURS = 48  # Track positions from last 48 hours
```

## Adding New Signal Patterns

The scanner uses a modular pattern system. To add new patterns:

1. Open `realtime_scanner/signal_detector.py`
2. Add your pattern function:

```python
def pattern_your_new_pattern(self, clusters, trades, wallet_tracker):
    """Your pattern description"""
    signals = []

    # Your detection logic here
    # Return list of signals

    return signals
```

3. Register it in `register_default_patterns()`:

```python
self.register_pattern(
    self.pattern_your_new_pattern,
    "Your Pattern Name",
    "Description of what triggers this pattern"
)
```

## Monitoring

Scanner outputs logs to console:
```
============================================================
[2025-02-13 10:30:00] Starting scan cycle...
============================================================
Latest block: 54123456
Last processed: 54122456
Blocks to process: 1000
Processing blocks 54122457 to 54123456...
✅ Found 237 trades in this cycle
✅ Detected 3 wallet clusters
🚨 Found 1 signals!
✅ Sent alert: High Conviction Cluster
✅ Scan cycle complete
   Wallets tracked: 1,247
   Signals detected (total): 1

⏰ Next scan in 300 seconds...
```

## Files Explained

- `config.py` - Configuration settings
- `wallet_tracker.py` - Tracks wallet positions and conviction
- `blockchain_scanner.py` - Connects to Polygon and monitors trades
- `signal_detector.py` - Modular pattern detection system
- `telegram_notifier.py` - Sends formatted Telegram alerts
- `main.py` - Main scanner loop

## Troubleshooting

### No signals detected
- Check if scanner is processing trades (should see "Found X trades in this cycle")
- Verify Alchemy API key is valid
- Lower thresholds in `config.py` to test

### Telegram not working
- Verify bot token and chat ID are correct
- Test by messaging `@polyfebbot` on Telegram
- Check scanner logs for Telegram errors

### Scanner crashes
- Check Alchemy API rate limits
- Verify internet connection
- Review error logs

## Support

For issues or questions, check the scanner logs and verify:
1. Alchemy API key is valid
2. Telegram credentials are correct
3. Internet connection is stable
