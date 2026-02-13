# 🚨 ACTION REQUIRED - Read This First

## What Just Happened

1. ✅ **Removed exposed Telegram credentials** from all files
2. ✅ **Updated scanner to optimal settings** (5+ wallets, $2K, 85% conviction)
3. ✅ **Added security and troubleshooting guides**

## Your To-Do List (5 minutes)

### Step 1: Regenerate Telegram Bot Token (URGENT)

Your old token is in git history, so regenerate it:

1. Open Telegram
2. Message `@BotFather`
3. Send: `/mybots`
4. Select: `polyfebbot`
5. Click: **"API Token"**
6. Click: **"Revoke current token"**
7. **Copy the new token**

### Step 2: Make GitHub Repo Private

1. Go to: https://github.com/BTBLABS24/polymarket-bot-clean
2. Click: **"Settings"**
3. Scroll down to: **"Danger Zone"**
4. Click: **"Change visibility"**
5. Select: **"Make private"**
6. Confirm

### Step 3: Update Your .env File

```bash
cd /private/tmp/polymarket-bot
cp .env.example .env
nano .env
```

Add your credentials:
```
ALCHEMY_API_KEY=your_alchemy_key
TELEGRAM_BOT_TOKEN=<NEW_TOKEN_FROM_STEP_1>
TELEGRAM_CHAT_ID=1563550509
```

### Step 4: Deploy to Railway (If Not Already Done)

**If you haven't deployed yet:**

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click: **"New Project"** → **"Deploy from GitHub repo"**
4. Select: `BTBLABS24/polymarket-bot-clean`
5. Add environment variables (Variables tab):
   ```
   ALCHEMY_API_KEY=your_key
   TELEGRAM_BOT_TOKEN=<new_token>
   TELEGRAM_CHAT_ID=1563550509
   ```
6. Wait 2-3 minutes for deployment

**If already deployed:**

1. Go to Railway dashboard
2. Select your project
3. Click: **"Variables"**
4. Update: `TELEGRAM_BOT_TOKEN` with NEW token
5. Railway will auto-redeploy

### Step 5: Test It Works

You should receive a Telegram message:
```
🤖 Real-Time Scanner Started

Monitoring Polygon blockchain for insider signals!
...
```

If you don't receive this, see: `TELEGRAM_BOT_TROUBLESHOOTING.md`

## Files to Read

1. **SECURITY_URGENT.md** - Full security details
2. **TELEGRAM_BOT_TROUBLESHOOTING.md** - If bot still not working
3. **WALLET_THRESHOLD_BACKTEST.md** - Why we changed to 5+ wallets

## What Changed in Configuration

Based on backtest results, updated to optimal settings:

| Setting | Old | New | Reason |
|---------|-----|-----|--------|
| MIN_WALLETS_CLUSTER | 1 | **5** | Historical minimum, 66.7% WR |
| MIN_WALLET_VOLUME | $1K | **$2K** | Higher quality signals |
| MIN_CONVICTION | 80% | **85%** | Reduce noise |

**Expected performance:** 66.7% win rate, +502% avg ROI per signal

## Push to GitHub

After completing steps above:

```bash
git push origin main
```

**Note:** The repo should be private before pushing!

## Questions?

- Bot not working? → Read `TELEGRAM_BOT_TROUBLESHOOTING.md`
- Security questions? → Read `SECURITY_URGENT.md`
- Want different thresholds? → Edit `realtime_scanner/config.py`

## Summary

✅ Code is clean and secure
⏰ Takes 5 minutes to:
   1. Regenerate bot token
   2. Make repo private
   3. Deploy/update Railway

Then you're done! Scanner will run 24/7 and send Telegram alerts.
