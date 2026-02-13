"""
Configuration for Real-Time Polymarket Scanner
"""
import os

# ========== API KEYS ==========
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# ========== BLOCKCHAIN CONFIG ==========
POLYGON_RPC = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
CTF_EXCHANGE = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"  # Polymarket CTF Exchange
BLOCK_BATCH_SIZE = 1000  # Process blocks in batches

# ========== SIGNAL DETECTION THRESHOLDS ==========
MIN_WALLET_VOLUME = 1000  # $1K minimum per wallet
MIN_CONVICTION = 0.80  # 80% of wallet capital on single position
MIN_WALLETS_CLUSTER = 1  # ANY high-conviction wallet = signal (was 5)
MAX_PRICE = 0.60  # Only bets ≤$0.60 (underdogs)
LOOKBACK_HOURS = 48  # Track positions from last 48 hours

# ========== SCANNER SETTINGS ==========
SCAN_INTERVAL_SECONDS = 300  # Scan every 5 minutes

# ========== CATEGORY FILTERS ==========
# Politics keywords (90% WR, 207% ROI)
POLITICS_KEYWORDS = [
    'trump', 'biden', 'president', 'congress', 'shutdown', 'government',
    'election', 'senate', 'speaker', 'vote', 'impeach', 'democrat',
    'republican', 'political', 'cabinet', 'senate', 'bill', 'veto'
]

# Financial keywords (100% WR, 3,471% ROI)
FINANCIAL_KEYWORDS = [
    'bank failure', 'fdic', 'bank seizure', 'silicon valley bank',
    'svb', 'first republic', 'signature bank', 'bailout', 'banking crisis',
    'fed', 'federal reserve', 'interest rate', 'recession'
]

# Exclude keywords (low performance categories)
EXCLUDE_KEYWORDS = [
    'bitcoin', 'btc', 'crypto', 'ethereum', 'eth', 'gold', 'silver',
    'game', 'nfl', 'nba', 'sports', 'super bowl', 'championship',
    'movie', 'oscar', 'grammy', 'award', 'actor', 'actress'
]
