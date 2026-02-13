# Telegram Bot Troubleshooting

## Issue: "Telegram bot still isn't working"

Let's diagnose and fix the issue systematically.

---

## Quick Diagnosis

### 1. Check If Scanner Is Running

**Where is it deployed?**
- [ ] Railway
- [ ] Local machine
- [ ] VPS/Server
- [ ] Not deployed yet

If not deployed yet, that's why it's not working! See deployment section below.

---

## Deployment Status Check

### Check Railway Deployment

1. Go to https://railway.app
2. Find your project: `polymarket-bot-clean`
3. Check status:
   - ✅ **Running** = Good
   - ⚠️ **Crashed** = Check logs
   - ⏸️ **Stopped** = Start it
   - ❌ **Not deployed** = Deploy it

4. View logs:
   - Click on your service
   - Check logs for:
     - `"REAL-TIME POLYMARKET SCANNER"` = Started successfully
     - `"✅ Connected"` = Alchemy + Telegram working
     - Errors = See error section below

---

## Common Issues & Fixes

### Issue 1: "No startup message in Telegram"

**Cause:** Scanner not running or Telegram credentials wrong

**Fix:**

1. **Verify credentials:**
   ```bash
   # Test bot token
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   ```

   Should return:
   ```json
   {"ok":true,"result":{"id":7989561870,"is_bot":true,"first_name":"polyfebbot"...}}
   ```

2. **Check chat ID:**
   - Message `@userinfobot` on Telegram
   - It replies with your chat ID
   - Verify it matches `1563550509`

3. **Test sending message:**
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_CHAT_ID>&text=Test"
   ```

---

### Issue 2: "Railway logs show errors"

**Common errors:**

#### Error: `ModuleNotFoundError: No module named 'telegram'`
**Fix:** Rebuild Railway project
- Railway → Settings → Redeploy

#### Error: `Alchemy API: ❌ Not configured`
**Fix:** Add `ALCHEMY_API_KEY` in Railway variables

#### Error: `Telegram: ❌ Not configured`
**Fix:** Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in Railway variables

#### Error: `Connection refused / timeout`
**Fix:** Check if Railway has internet access (should be fine)

---

### Issue 3: "Scanner runs but no signals"

**This is normal!**

Signals are rare:
- Expected: ~1-2 signals per day
- Scanner checks every 5 minutes
- Most cycles find 0 signals

**Check logs for:**
```
Starting scan cycle...
Latest block: 54123456
Found 237 trades in this cycle
✅ Detected 3 wallet clusters
🚨 Found 0 signals!  <-- This is normal most of the time
```

If you see this, scanner is **working correctly** but no signals meet criteria yet.

---

### Issue 4: "Can't access Railway / Forgot to deploy"

**Solution: Deploy to Railway**

1. **Sign up for Railway:**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy:**
   - New Project → Deploy from GitHub repo
   - Select: `BTBLABS24/polymarket-bot-clean`
   - Railway auto-detects Dockerfile

3. **Add environment variables:**
   - Click project → Variables tab
   - Add:
     ```
     ALCHEMY_API_KEY=your_alchemy_key
     TELEGRAM_BOT_TOKEN=your_bot_token
     TELEGRAM_CHAT_ID=1563550509
     ```

4. **Wait for deployment:**
   - Takes ~2-3 minutes
   - Check logs for startup message

5. **Verify:**
   - Should receive Telegram message: "Real-Time Scanner Started"

---

## Testing Locally (Alternative to Railway)

If Railway isn't working, test locally first:

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export ALCHEMY_API_KEY="your_key"
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="1563550509"
```

### 3. Run Scanner
```bash
cd realtime_scanner
python3 main.py
```

### 4. Expected Output
```
============================================================
REAL-TIME POLYMARKET SCANNER
============================================================
Alchemy API: ✅ Connected
Telegram: ✅ Connected
Scan interval: Every 300 seconds
Min wallet volume: $1000
Min conviction: 80.0%
Min wallets for signal: 1 (ANY wallet counts!)
============================================================

Starting scan cycle...
```

### 5. Check Telegram
Should receive: "🤖 Real-Time Scanner Started"

---

## Verification Checklist

Run through this checklist:

- [ ] **Bot token is valid**
  - Test: `curl https://api.telegram.org/bot<TOKEN>/getMe`
  - Should return bot info

- [ ] **Chat ID is correct**
  - Message `@userinfobot` to verify
  - Should match `1563550509`

- [ ] **Scanner is deployed**
  - Railway dashboard shows "Running"
  - OR local `python3 main.py` is running

- [ ] **Environment variables set**
  - Railway: Variables tab shows all 3 variables
  - OR local: `echo $TELEGRAM_BOT_TOKEN` shows token

- [ ] **Dependencies installed**
  - `pip3 list | grep telegram` shows `python-telegram-bot`
  - `pip3 list | grep web3` shows `web3`

- [ ] **Network connectivity**
  - Scanner can reach Telegram API
  - Scanner can reach Alchemy API

---

## Most Likely Issue

Based on "bot still isn't working", most common causes:

### 1. Scanner Not Deployed (80% of cases)
**Fix:** Deploy to Railway following steps above

### 2. Wrong Credentials in Railway (15% of cases)
**Fix:** Check Railway Variables tab, ensure all 3 are set correctly

### 3. Bot Token Needs Regenerating (5% of cases)
**Fix:** After credentials were exposed, generate new token from @BotFather

---

## Step-by-Step Fix

### Option A: Fresh Railway Deployment

1. **Regenerate bot token:**
   - Message `@BotFather` on Telegram
   - `/mybots` → Select bot → API Token → Revoke
   - Copy NEW token

2. **Make repo private:**
   - GitHub → Settings → Change visibility → Private

3. **Deploy to Railway:**
   - Railway.app → New Project
   - Deploy from GitHub: `polymarket-bot-clean`
   - Add variables:
     ```
     ALCHEMY_API_KEY=<your_alchemy_key>
     TELEGRAM_BOT_TOKEN=<new_token_from_step_1>
     TELEGRAM_CHAT_ID=1563550509
     ```

4. **Wait 2-3 minutes**

5. **Check Telegram for startup message**

### Option B: Local Testing First

1. Regenerate bot token (see step 1 above)

2. Create `.env` file:
   ```bash
   cd /private/tmp/polymarket-bot
   cp .env.example .env
   nano .env
   ```

3. Add credentials to `.env`

4. Install and run:
   ```bash
   pip3 install -r requirements.txt
   export $(cat .env | xargs)
   cd realtime_scanner
   python3 main.py
   ```

5. If you get startup message in Telegram, it works!

6. Then deploy to Railway for 24/7 operation

---

## Getting Help

Still not working? Provide this info:

1. **Where is scanner running?**
   - Railway / Local / Not running

2. **What do Railway logs show?** (if using Railway)
   - Copy last 20 lines of logs

3. **Did you receive ANY Telegram messages?**
   - Yes: What message?
   - No: Did you test the bot token with curl?

4. **Environment variables set?**
   - Railway: Screenshot of Variables tab
   - Local: `echo $TELEGRAM_BOT_TOKEN` (hide actual token)

---

## Next Steps After Working

Once you get the startup message:

1. ✅ Scanner is working
2. ⏰ Wait for signals (1-2 per day expected)
3. 📊 Check logs to see scanning activity
4. 🎯 When signal arrives, check Kalshi and place bet

Scanner checks every 5 minutes automatically.
