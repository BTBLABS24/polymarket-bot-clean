# Quick Start Guide

## What Was Built

A **real-time blockchain scanner** that monitors Polygon for Polymarket insider signals:

- ✅ Monitors Polygon blockchain via Alchemy (every 5 minutes)
- ✅ Tracks individual wallet positions and conviction levels
- ✅ Detects when **5+ wallets** (each $1K+) put **80%+ of capital** on same bet
- ✅ Sends Telegram alerts for Politics (90% WR, 207% ROI) & Financial (100% WR, 3,471% ROI)
- ✅ Modular pattern system - easy to add new signal types
- ✅ Persists state across restarts

## Deploy in 5 Minutes (Railway)

### 1. Get Alchemy API Key

1. Go to https://www.alchemy.com/
2. Sign up (free)
3. Create app: **Polygon Mainnet**
4. Copy API key

### 2. Deploy to Railway

1. Go to https://railway.app
2. Sign up/login (free)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select: `BTBLABS24/polymarket-bot-clean`
5. Railway auto-detects Dockerfile and deploys

### 3. Add Environment Variables

In Railway dashboard:
- Click your service
- Go to "Variables" tab
- Add:
  ```
  ALCHEMY_API_KEY=your_alchemy_key_here
  TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
  ```

### 4. Verify It's Running

1. Check Railway logs: Should see "REAL-TIME POLYMARKET SCANNER"
2. Check Telegram: Should receive "Real-Time Scanner Started" message
3. Done! Scanner checks every 5 minutes

## Test Locally (Optional)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run test
python3 test_setup.py

# Set environment variables
export ALCHEMY_API_KEY="your_key"
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

# Run scanner
cd realtime_scanner
python3 main.py
```

## How It Works

```
1. Scanner connects to Polygon blockchain via Alchemy
   ↓
2. Monitors Polymarket CTF Exchange for trades
   ↓
3. Tracks wallet positions:
   - Each wallet's total volume
   - Conviction = position_volume / total_volume
   ↓
4. Detects clusters:
   - 5+ wallets
   - Each with $1K+ volume
   - Each with 80%+ conviction
   - Same market + outcome
   ↓
5. Filters by category:
   - Politics (90% WR, 207% ROI)
   - Financial (100% WR, 3,471% ROI)
   ↓
6. Sends Telegram alert with:
   - Event name & outcome
   - Entry price & ROI
   - Number of wallets & total volume
   - Recommended position size
   - Historical performance stats
```

## Example Alert

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

## Architecture

```
realtime_scanner/
├── config.py              # Configuration (thresholds, keywords)
├── wallet_tracker.py      # Track wallet positions & conviction
├── blockchain_scanner.py  # Connect to Polygon & get trades
├── signal_detector.py     # Modular pattern detection
├── telegram_notifier.py   # Send formatted alerts
└── main.py               # Main loop (runs every 5 min)
```

## Current Signal Patterns

1. **High Conviction Cluster** (YOUR MAIN PATTERN)
   - 5+ wallets with $1K+, 80%+ conviction
   - Same market + outcome
   - Politics or Financial only
   - Price ≤ $0.60

2. **Whale Entry**
   - Single wallet $10K+ with 80%+ conviction
   - Entered within last hour

3. **Synchronized Entry**
   - 5+ wallets entering within 1 hour
   - Suggests coordinated/insider activity

## Adding New Patterns

Edit `realtime_scanner/signal_detector.py`:

```python
def pattern_your_new_pattern(self, clusters, trades, wallet_tracker):
    """Your pattern description"""
    signals = []

    # Your detection logic
    for cluster in clusters:
        if your_condition:
            signals.append({
                'type': 'your_type',
                'conviction': 'HIGH',
                'cluster': cluster
            })

    return signals

# Register it
self.register_pattern(
    self.pattern_your_new_pattern,
    "Your Pattern Name",
    "Description"
)
```

## Configuration

Edit `realtime_scanner/config.py`:

```python
MIN_WALLET_VOLUME = 1000    # $1K per wallet
MIN_CONVICTION = 0.80       # 80% focus
MIN_WALLETS_CLUSTER = 5     # 5+ wallets = signal
MAX_PRICE = 0.60           # Only underdogs
SCAN_INTERVAL_SECONDS = 300 # 5 minutes
LOOKBACK_HOURS = 48        # 48 hour window
```

## Monitoring

**Railway Dashboard:**
- View logs in real-time
- See deployment status
- Check resource usage
- Restart if needed

**Expected log output:**
```
============================================================
REAL-TIME POLYMARKET SCANNER
============================================================
Alchemy API: ✅ Connected
Telegram: ✅ Connected
Scan interval: Every 300 seconds
Min wallet volume: $1000
Min conviction: 80.0%
Min wallets for signal: 5
============================================================

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

## Troubleshooting

**No Telegram startup message:**
- Check Railway logs for errors
- Verify bot token is correct
- Message @polyfebbot to test

**No signals detected:**
- This is normal! Signals are rare (2/week)
- Check logs show "Found X trades" (means it's working)
- To test: lower MIN_WALLETS_CLUSTER to 2 in config.py

**Scanner crashes:**
- Check Railway logs for Python errors
- Verify Alchemy API key is valid
- Check Alchemy rate limits

**Can't connect to Alchemy:**
- Verify API key is for Polygon Mainnet
- Check Alchemy dashboard for issues
- Test locally first

## Cost

- **Railway:** $0/month (free tier sufficient)
- **Alchemy:** $0/month (free tier sufficient)
- **Total:** $0/month

Monitor dashboards to stay within free tiers.

## Next Steps

1. Deploy to Railway (5 minutes)
2. Verify Telegram startup message
3. Wait for signals (2/week expected)
4. When signal arrives, check Kalshi for the market
5. Place bet manually with recommended position size

## Files

- `README.md` - Complete documentation
- `DEPLOYMENT.md` - Detailed deployment guides (Railway/VPS/Docker)
- `QUICKSTART.md` - This file
- `test_setup.py` - Local test script
- `.env.example` - Environment variable template

## Support

For detailed deployment instructions, see `DEPLOYMENT.md`.

For troubleshooting, check Railway logs first, then verify:
1. Environment variables are set
2. Alchemy API key is valid (Polygon Mainnet)
3. Telegram bot token is correct

---

**Ready to deploy?** → See step-by-step guide in `DEPLOYMENT.md`
