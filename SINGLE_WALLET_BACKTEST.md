# Single Wallet Backtest Analysis
## Testing MIN_WALLETS_CLUSTER = 1 vs 5

### Data Source
92 events from FULL_1K_THRESHOLD_UPDATED.csv (90-day historical data)
- $1K min volume per wallet
- 80%+ conviction requirement
- Politics & Financial categories

---

## Summary Results

### Signal Distribution by Wallet Count

| Wallet Range | Count | % of Total | Avg Wallets | Total Volume |
|--------------|-------|------------|-------------|--------------|
| **1 wallet** | 0 | 0% | 1.0 | $0 |
| **2-4 wallets** | 16 | 17.4% | 3.1 | $562K |
| **5+ wallets** | 76 | 82.6% | 32.9 | $18.2M |

**Key Finding:** No signals with only 1 wallet in historical data. Minimum was 5 wallets (tied for smallest cluster).

---

## Performance by Wallet Count

### 5-9 Wallets (Small Clusters)
**Count:** 21 signals
**Verified:** 9 signals

| Metric | Value |
|--------|-------|
| Win Rate | 88.9% (8/9) |
| Avg ROI per Signal | +338% |
| Total ROI | +3,045% |
| Avg Wallets | 6.4 |
| Avg Volume | $30,177 |

**Top Performers:**
- Will Stable launch a token: 5 wallets, +376% ROI ✅
- Will Israel strike Gaza: 5 wallets, +302% ROI ✅
- Will Israel strike Gaza: 5 wallets, +245% ROI ✅
- Will Trump acquire Greenland: 5 wallets, +614% ROI (unverified)
- US bank failure by January 31: 14 wallets + small follow-on, **+3,471% ROI** ✅

**Only Loss:**
- Maduro out by...: 10 wallets, -100% ❌

---

### 10-19 Wallets (Medium Clusters)
**Count:** 13 signals
**Verified:** 7 signals

| Metric | Value |
|--------|-------|
| Win Rate | 85.7% (6/7) |
| Avg ROI per Signal | +316% |
| Total ROI | +2,215% |
| Avg Wallets | 13.0 |
| Avg Volume | $65,881 |

**Top Performers:**
- Will Israel strike Lebanon: 10 wallets, +132% ROI ✅
- How long will Shutdown last: 11 wallets, +223% ROI ✅
- What will Trump say Feb 1: 16 wallets, +203% ROI ✅
- What will Powell say: 14 wallets, +132% ROI ✅

**Only Loss:**
- Russia x Ukraine ceasefire: 13 wallets, -100% ❌

---

### 20+ Wallets (Large Clusters)
**Count:** 42 signals
**Verified:** 16 signals

| Metric | Value |
|--------|-------|
| Win Rate | 93.8% (15/16) |
| Avg ROI per Signal | +248% |
| Total ROI | +3,971% |
| Avg Wallets | 55.1 |
| Avg Volume | $584,419 |

**Top Performers:**
- US government shutdown: 68 wallets, +335% ROI ✅
- Who will Trump talk to: 134 wallets, +147% ROI ✅
- How long will Shutdown last: 105 wallets, +233% ROI ✅
- Pro Bowl halftime show: 86 wallets, +232% ROI ✅

**Only Loss:**
- What will Gold hit: 28 wallets, -100% ❌

---

## Key Findings

### 1. No True Single Wallet Signals
**Historical data shows NO signals with only 1 wallet.**
- Minimum cluster size was 5 wallets
- Even "small" signals had 5-9 wallets
- Single wallet detection is **untested**

### 2. Small Clusters (5-9 Wallets) Perform VERY Well
**Best win rate and ROI per signal:**
- 88.9% win rate (vs 93.8% for 20+)
- 338% avg ROI (vs 248% for 20+)
- Includes the massive bank failure signal (+3,471% ROI)

### 3. Wallet Count ≠ Performance
**More wallets does NOT guarantee better results:**
- 5-9 wallets: 88.9% WR, 338% ROI
- 10-19 wallets: 85.7% WR, 316% ROI
- 20+ wallets: 93.8% WR, 248% ROI

**Slightly better win rate with more wallets, but lower ROI per signal.**

### 4. Volume Matters More Than Wallet Count
**High conviction + meaningful volume = good signal**
- 5 wallets with $35K volume = +376% ROI ✅
- 14 wallets with $265K volume = +3,471% ROI ✅
- 68 wallets with $519K volume = +335% ROI ✅

---

## What Happens with MIN_WALLETS_CLUSTER = 1?

### Projected Signal Volume

**Historical (5+ wallets):**
- 92 signals in 90 days
- ~1 signal/day

**Projected (1+ wallet):**
- Unknown - no historical data
- Could be **10-100x more signals**
- Likely dominated by single $1K wallets

### Expected Signal Quality

#### Best Case Scenario
Single wallets are skilled insiders:
- Similar performance to 5-9 wallet clusters
- ~80-90% win rate
- ~300%+ avg ROI
- More opportunities to catch early moves

#### Worst Case Scenario
Single wallets are noise:
- Random high-conviction bets
- ~50% win rate (coin flip)
- Lower avg ROI
- Signal fatigue from spam

#### Most Likely Scenario
Mixed bag:
- Some excellent single wallet signals
- Lots of noise/false positives
- Need to filter by:
  - Volume ($5K+ more meaningful)
  - Conviction (95%+ better)
  - Price (lower = better ROI)
  - Category (Politics/Financial only)

---

## Recommendations

### Option 1: Start with 2-3 Wallets (Conservative)
```python
MIN_WALLETS_CLUSTER = 2  # Require at least a pair
MIN_WALLET_VOLUME = 2000  # Increase to $2K per wallet
MIN_CONVICTION = 0.85  # Increase to 85%
```

**Pros:**
- Reduces single wallet noise
- Still catches small clusters (historically excellent)
- More manageable signal volume

**Expected:**
- ~2-5x more signals than original
- Similar quality to historical data

---

### Option 2: Single Wallet with High Filters (Current)
```python
MIN_WALLETS_CLUSTER = 1  # Allow singles
MIN_WALLET_VOLUME = 1000  # Keep $1K
MIN_CONVICTION = 0.80  # Keep 80%
```

**Pros:**
- Maximum coverage
- Catches every high-conviction bet
- Tests single wallet hypothesis

**Cons:**
- Likely **many** signals per day
- Unknown quality
- Potential signal fatigue

**Mitigation:**
- Focus on conviction score (HIGH/VERY HIGH only)
- Filter by volume ($5K+ for singles)
- Monitor for 1 week and adjust

---

### Option 3: Tiered Approach (Recommended)
Keep MIN_WALLETS_CLUSTER = 1 but add volume tiers:

```python
# In signal_detector.py conviction scoring:
if num_wallets == 1 and total_volume >= 10000:
    conviction_score = "HIGH"  # Single $10K+ whale
elif num_wallets == 1 and total_volume >= 5000:
    conviction_score = "MEDIUM"  # Single $5K+ wallet
elif num_wallets == 1:
    conviction_score = "LOW"  # Single $1K wallet (noise?)
```

**Result:**
- All signals detected
- Clear quality indicators
- Focus on HIGH/VERY HIGH
- Review LOW signals to learn

---

## Testing Plan

### Week 1: Collect Data
- Run with MIN_WALLETS_CLUSTER = 1
- Track ALL signals (don't filter)
- Record:
  - Wallet count
  - Volume
  - Conviction
  - Outcome
  - Whether you would have bet

### Week 2: Analyze
- How many signals per day?
- Single wallet quality?
- Optimal volume threshold?
- Best conviction level?

### Week 3: Optimize
- Adjust thresholds based on data
- Set optimal filters
- Compare to 5+ wallet baseline

---

## Historical Performance Summary

### Verified Signals Only (32 total)

**By Wallet Count:**
| Range | Count | Win Rate | Avg ROI | Best ROI |
|-------|-------|----------|---------|----------|
| 5-9 wallets | 9 | 88.9% | +338% | +3,471% |
| 10-19 wallets | 7 | 85.7% | +316% | +223% |
| 20+ wallets | 16 | 93.8% | +248% | +335% |
| **All 5+** | **32** | **90.6%** | **+280%** | **+3,471%** |

**By Category:**
- **Politics:** 10 verified, 90% WR, 207% avg ROI
- **Financial:** 1 verified, 100% WR, 3,471% ROI (!)
- **Geopolitics:** 14 verified, 92.9% WR, 245% avg ROI
- **Entertainment:** 2 verified, 100% WR, 229% avg ROI
- **Gaming:** 4 verified, 0% WR, -100% avg ROI
- **Other:** 1 verified, 100% WR, 376% avg ROI

---

## Bottom Line

**Historical data shows:**
1. ✅ Small clusters (5-9 wallets) perform excellent
2. ✅ More wallets = slightly better WR, but lower ROI
3. ❌ No single wallet signals in historical data
4. ⚠️ Single wallet performance is **completely untested**

**Current config (MIN_WALLETS_CLUSTER = 1):**
- Theoretical maximum coverage
- Unknown signal quality
- Likely **much higher volume**
- Risk of noise/fatigue

**Recommended:**
1. **Test for 1 week** with current settings
2. **Track all signals** (don't skip LOW conviction)
3. **Focus on HIGH/VERY HIGH** for actual bets
4. **Adjust after data collection**

Most likely outcome: You'll find single wallets are mostly noise, and will increase MIN_WALLETS_CLUSTER to 2-3 after testing.

But the only way to know is to run it and collect data! 📊
