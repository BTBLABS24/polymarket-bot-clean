# Changelog

## [2025-02-13] - No Minimum Wallet Requirement

### Changed
- **MIN_WALLETS_CLUSTER: 5 → 1**
  - Scanner now detects **ANY wallet** with high conviction
  - No longer requires 5+ wallets clustering on same bet
  - Single wallets with $1K+ volume and 80%+ conviction will trigger alerts

### Impact

**Before:** Only signaled when 5+ wallets converged on same bet
- Missed single whale entries
- Missed 2-4 wallet clusters
- More conservative (fewer signals)

**After:** Signals on ANY high-conviction wallet
- Catches all $1K+ wallets with 80%+ conviction
- Includes single wallets, pairs, small groups
- More aggressive (more signals)

### Conviction Scoring (Updated)

New multi-factor scoring for flexibility:

- **VERY HIGH:** 20+ wallets + price < $0.30, OR 10+ wallets + price < $0.40
- **HIGH:** 5+ wallets + price < $0.50, OR 3+ wallets + 90%+ conviction
- **MEDIUM:** 2+ wallets + $5K+ volume, OR 1 wallet + $5K+ volume + 90%+ conviction
- **LOW:** Any other high-conviction signal

### Expected Signal Volume

**Original (5+ wallets):**
- ~2 signals/week for Politics
- Very rare for Financial

**Updated (1+ wallet):**
- Likely **10-20x more signals**
- Will include many single wallets
- More noise but catches everything
- Use conviction score to filter

### Recommendations

1. **Test first:** Run for a few days and monitor signal volume
2. **Filter by conviction:** Focus on HIGH/VERY HIGH signals
3. **Adjust if needed:** Can increase MIN_WALLET_VOLUME to reduce noise
4. **Consider volume:** Single wallets with $5K+ are more meaningful

### Adjusting Signal Sensitivity

If you get too many signals, edit `realtime_scanner/config.py`:

```python
# Reduce signals - require higher volume per wallet
MIN_WALLET_VOLUME = 2000  # Increase from 1000

# Reduce signals - require higher conviction
MIN_CONVICTION = 0.90  # Increase from 0.80

# Reduce signals - require multiple wallets again
MIN_WALLETS_CLUSTER = 3  # Increase from 1
```

### Deployment

Changes already pushed to GitHub: `BTBLABS24/polymarket-bot-clean`

If deployed on Railway:
- Railway will auto-deploy from GitHub
- No configuration changes needed
- Check logs to verify new version deployed
- Should see: "Min wallets for signal: 1 (ANY wallet counts!)"

### Testing Locally

```bash
# Pull latest changes
git pull

# Verify config
python3 test_setup.py
# Should show: "Min Wallets for Cluster: 1"

# Run scanner
cd realtime_scanner
python3 main.py
```

### Example Alerts

**Single Wallet ($1K, 90% conviction):**
```
🚨 NEW HIGH CONVICTION SIGNAL 🚨

Pattern: Wallet(s) with $1K+ volume, 80%+ conviction on same outcome

Event: Trump announces Greenland purchase?
Outcome: YES

💰 Entry Price: $0.120 (12.0%)
📊 Potential ROI: +733%
👥 Wallets: 1 high-conviction wallet
💵 Total Volume: $1,200
🎯 Conviction: 92%

📈 Recommended Position: 5% of portfolio

Category: Politics
🎯 Conviction: MEDIUM
```

**Large Single Wallet ($10K, 95% conviction):**
```
🚨🚨 NEW HIGH CONVICTION SIGNAL 🚨🚨

Pattern: Wallet(s) with $1K+ volume, 80%+ conviction on same outcome

Event: Bank failure this quarter?
Outcome: YES

💰 Entry Price: $0.250 (25.0%)
📊 Potential ROI: +300%
👥 Wallets: 1 high-conviction wallet
💵 Total Volume: $12,500
🎯 Conviction: 95%

📈 Recommended Position: 7% of portfolio

Category: Financial
🎯 Conviction: HIGH
```

### Reverting Changes

If you want to go back to 5+ wallet requirement:

```python
# realtime_scanner/config.py
MIN_WALLETS_CLUSTER = 5  # Change from 1
```

Then commit and push:
```bash
git add realtime_scanner/config.py
git commit -m "Revert to 5+ wallet requirement"
git push
```
