# Deployment Guide

## Quick Start (Railway - Recommended)

Railway provides the easiest deployment with persistent services and automatic restarts.

### 1. Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Alchemy API key (get from https://www.alchemy.com/)
- Your Telegram credentials (already have: bot token `YOUR_TELEGRAM_BOT_TOKEN`, chat ID `YOUR_TELEGRAM_CHAT_ID`)

### 2. Deploy to Railway

#### Option A: Deploy from GitHub (Recommended)

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Add real-time scanner"
   git push
   ```

2. **Create Railway project:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Dockerfile

3. **Set environment variables:**
   - In Railway dashboard, go to your service
   - Click "Variables" tab
   - Add these variables:
     ```
     ALCHEMY_API_KEY=your_alchemy_api_key
     TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
     TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
     ```

4. **Deploy:**
   - Railway will automatically build and deploy
   - Check logs to verify scanner is running
   - You should receive a Telegram message "Real-Time Scanner Started"

#### Option B: Deploy from CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project (or create new one)
railway init

# Set environment variables
railway variables set ALCHEMY_API_KEY=your_key
railway variables set TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
railway variables set TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID

# Deploy
railway up
```

### 3. Verify Deployment

1. Check Railway logs: Should see "REAL-TIME POLYMARKET SCANNER" startup message
2. Check Telegram: Should receive "Real-Time Scanner Started" message
3. Monitor for signals: Scanner checks every 5 minutes

### 4. Monitor & Maintain

**View logs:**
- Railway Dashboard → Your Service → Logs

**Restart scanner:**
- Railway Dashboard → Your Service → Settings → Restart

**Update code:**
```bash
git add .
git commit -m "Update scanner"
git push
# Railway auto-deploys on push
```

## Alternative: VPS Deployment

If you prefer to deploy on your own server (AWS, DigitalOcean, etc.):

### 1. Setup Server

```bash
# SSH into your server
ssh user@your-server

# Clone repo
git clone <your-repo-url>
cd polymarket-bot

# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3-pip

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file
cp .env.example .env
nano .env

# Add your keys:
# ALCHEMY_API_KEY=your_key
# TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
# TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID

# Load environment
export $(cat .env | xargs)
```

### 3. Run Scanner

**Option A: With nohup (simple)**
```bash
cd realtime_scanner
nohup python3 main.py > scanner.log 2>&1 &

# Check it's running
tail -f scanner.log
```

**Option B: With systemd (recommended)**

Create `/etc/systemd/system/polymarket-scanner.service`:
```ini
[Unit]
Description=Polymarket Real-Time Scanner
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user/polymarket-bot/realtime_scanner
Environment="ALCHEMY_API_KEY=your_key"
Environment="TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN"
Environment="TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID"
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable polymarket-scanner
sudo systemctl start polymarket-scanner
sudo systemctl status polymarket-scanner

# View logs
sudo journalctl -u polymarket-scanner -f
```

## Alternative: Docker Deployment

### 1. Build Image

```bash
docker build -t polymarket-scanner .
```

### 2. Run Container

```bash
docker run -d \
  --name polymarket-scanner \
  --restart unless-stopped \
  -e ALCHEMY_API_KEY="your_key" \
  -e TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" \
  -e TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID" \
  -v $(pwd)/data:/app/realtime_scanner \
  polymarket-scanner
```

### 3. Manage Container

```bash
# View logs
docker logs -f polymarket-scanner

# Restart
docker restart polymarket-scanner

# Stop
docker stop polymarket-scanner

# Remove
docker rm polymarket-scanner
```

## Troubleshooting

### No Telegram startup message

1. Check Railway/server logs for errors
2. Verify Telegram credentials are correct
3. Test bot by messaging `@polyfebbot`
4. Check bot token hasn't expired

### Scanner not detecting trades

1. Verify Alchemy API key is valid
2. Check Alchemy dashboard for API usage/rate limits
3. Review scanner logs for blockchain connection errors
4. Test Alchemy connection: `cd realtime_scanner && python3 -c "from blockchain_scanner import BlockchainScanner; s = BlockchainScanner(); print(s.get_latest_block())"`

### Scanner crashes/restarts

1. Check logs for Python errors
2. Verify all dependencies installed: `pip3 install -r requirements.txt`
3. Check server resources (RAM, disk space)
4. Review Alchemy API rate limits

### No signals detected

This is normal! Signals are rare (2/week for Politics). The scanner is working if:
- Logs show "Starting scan cycle..."
- Logs show "Found X trades in this cycle"
- No errors in logs

To test signal detection, temporarily lower thresholds in `realtime_scanner/config.py`:
```python
MIN_WALLETS_CLUSTER = 2  # Lower from 5
MIN_WALLET_VOLUME = 100  # Lower from 1000
```

### Railway-specific issues

**Build fails:**
- Check Dockerfile syntax
- Verify all files committed to git
- Check Railway build logs

**Service crashes:**
- Check Railway logs for Python errors
- Verify environment variables are set
- Check if free tier limits exceeded

**Can't see logs:**
- Railway Dashboard → Your Service → Logs
- May need to wait ~30s for logs to appear

## Cost Estimates

### Railway
- Free tier: $5/month credit (sufficient for this scanner)
- Pro tier: $20/month if you exceed free tier
- This scanner should stay within free tier

### Alchemy
- Free tier: 300M compute units/month (sufficient)
- Growth tier: $49/month if you exceed free tier
- This scanner uses ~1-2M compute units/day

### Total Cost
- **$0/month** if staying within free tiers
- Monitor usage in dashboards to avoid surprises

## Getting Your Alchemy API Key

1. Go to https://www.alchemy.com/
2. Sign up for free account
3. Create new app:
   - Chain: Polygon
   - Network: Polygon Mainnet
4. Copy API key from dashboard
5. Add to Railway environment variables or `.env` file

## Support

If you encounter issues:

1. Check logs first (Railway dashboard or `scanner.log`)
2. Verify all environment variables are set correctly
3. Test locally first: `cd realtime_scanner && python3 main.py`
4. Check Alchemy dashboard for API issues
5. Test Telegram bot by messaging it directly
