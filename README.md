# Quantitative Evaluation of the SuperTrend Indicator on Indian Equities

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)](https://www.postgresql.org/)
[![Data](https://img.shields.io/badge/Data-NSE%2FBSE-green.svg)](https://www.nseindia.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Research Focus:** Backtesting the SuperTrend technical indicator on Indian stock market data to evaluate signal reliability, parameter sensitivity, and sector-specific effectiveness.

**Status:** Analysis complete. Historical backtesting only. No live trading or real-time features.

## 📋 Project Overview

### Business Problem
Can the SuperTrend indicator generate consistent signals across different sectors of the Indian stock market? How does parameter tuning affect signal accuracy?

### Research Question
What is the relationship between SuperTrend indicator parameters (length and ATR factor) and signal accuracy across NSE-listed equities?

### Objectives
1. Implement SuperTrend indicator with multiple parameter configurations
2. Backtest signals on NIFTY 500 stocks using historical weekly data
3. Compare signal accuracy between (7,1) aggressive and (10,2) conservative parameters
4. Analyze sector-specific performance and signal reliability
5. Visualize results through Power BI dashboard

### Data Scope
- **Time Period:** 2015-2024 (10 years of weekly data)
- **Universe:** NIFTY 500 stocks (~500 companies)
- **Data Source:** Yahoo Finance weekly OHLC prices
- **Geographic Focus:** National Stock Exchange (NSE), India

---

## 🏗️ Project Architecture

```
Yahoo Finance / NSE APIs
        ↓
1_collection/ - Data Fetching
(fetch_prices.py, compute_sector_returns.py)
        ↓
CSV Storage
(nse_history_csv/, nse_securities/)
        ↓
2_loading/ - PostgreSQL Loading
(load_nse_trade.py, load_nse_sec.py)
        ↓
PostgreSQL Database
(nse_trade_daily, nse_securities, sector data)
        ↓
5_strategy/ - SuperTrend Calculation
(1_supertrend_signals.py, 3_compare_parameters.py)
        ↓
Signal Generation & Trade Simulation
(all_trades.csv)
        ↓
4_eda/ + 5_strategy/ - Analysis
(4_sector_analysis.py)
        ↓
Result CSVs
(final_summary_10_2.csv, final_summary_7_1.csv)
        ↓
6_dashboard/ - Power BI Visualization
(power_bi_supertrend_01.pbix)
```

---

## 📁 Repository Structure

```
stock_market_analysis/
├── 1_collection/              Data fetching scripts
│   ├── fetch_prices.py        Download NIFTY 500 weekly data
│   └── compute_sector_returns.py Calculate sector-level returns
├── 2_loading/                 Database loading scripts
│   ├── load_nse_trade.py      Load trade data into PostgreSQL
│   └── load_nse_sec.py        Load security master
├── 3_daily_updates/           Maintenance scripts
│   ├── run_daily_update.py    Orchestrate daily updates
│   └── update_log.txt         Update execution log
├── 4_eda/                     Exploratory analysis (incomplete)
│   └── 1_sector_trend_analysis.py Sector visualization attempts
├── 5_strategy/                Core analysis scripts
│   ├── 1_supertrend_signals.py Calculate SuperTrend for single stock
│   ├── 2_supertrend_all_stocks.py Batch processing (commented)
│   ├── 3_compare_parameters.py Compare (7,1) vs (10,2)
│   ├── 4_sector_analysis.py   Group results by industry
│   └── 5_visual_check.py      Plot SuperTrend visualization
├── 6_dashboard/               Power BI dashboards
│   ├── power_bi_supertrend_01.pbix Main dashboard
│   └── dashboard_1.png        Dashboard screenshot
├── data/securities/           Output files
│   ├── final_summary_10_2.csv Results with (10,2) parameters
│   ├── final_summary_7_1.csv  Results with (7,1) parameters
│   ├── nifty500.csv           Stock list with sector mapping
│   ├── sector_returns.csv     Weighted sector returns
│   └── all_trades.csv         Detailed trade list
├── nse_history_csv/           Historical price data (~500 CSV files)
└── README.md / DOCUMENTATION.md

```

---

## 📊 Dataset Description

### Source Files

| Dataset | Format | Records | Purpose |
|---------|--------|---------|---------|
| NIFTY 500 List | CSV | 500 stocks | Security universe and sector mapping |
| Weekly Prices | CSV | 192,651 rows | OHLC data from Yahoo Finance |
| NSE Securities | CSV | 2,230 | NSE security master (ISIN, listing date) |
| Historical Trade Data | CSV files | ~4,000+ files | Individual stock price history |

### Generated Output Files

| File | Rows | Content |
|------|------|---------|
| `final_summary_10_2.csv` | 545 | SuperTrend results with length=10, factor=2 |
| `final_summary_7_1.csv` | 1,962 | SuperTrend results with length=7, factor=1 |
| `all_trades.csv` | 62,716 | Individual trade records with entry/exit |
| `sector_returns.csv` | 10,461 | Weekly sector-level returns |

### Database Tables

PostgreSQL `stock_market_analysis` schema:
- `nse_trade_daily` - Daily OHLCV data (~1.8M records)
- `nse_securities` - Security master with metadata
- Supporting tables for block deals, bulk deals (not actively used)

---

## 🔬 Methodology

### 1. Data Collection
- Downloaded weekly OHLC data for NIFTY 500 stocks via Yahoo Finance API
- Period: 2015-01-05 to 2024-12-31 (10 years)
- Data stored in PostgreSQL for efficient querying

### 2. Data Processing
- Calculated weekly returns as: `(Close - Open) / Open`
- Computed market-cap weighted sector returns using share counts from Yahoo Finance
- Handled missing data by skipping incomplete records

### 3. SuperTrend Indicator Calculation

**True Range (TR):**
```
TR = MAX(High - Low, |High - PrevClose|, |Low - PrevClose|)
```

**Average True Range (ATR):**
```
ATR = SMA(TR, length)
```

**SuperTrend Bands:**
```
Middle = (High + Low) / 2
UpperBand = Middle + (factor × ATR)
LowerBand = Middle - (factor × ATR)
```

**Trend Logic:**
- If Close > UpperBand → UPTREND (SuperTrend = LowerBand)
- If Close < LowerBand → DOWNTREND (SuperTrend = UpperBand)

### 4. Signal Generation
- **BUY Signal:** Price closes above SuperTrend after being below
- **SELL Signal:** Price closes below SuperTrend after being above
- Holding period: Entire trend until reversal signal

### 5. Accuracy Measurement
```
Accuracy = (Profitable Trades / Total Trades) × 100%
```

### 6. Classification

Stocks categorized by signal reliability:
- **Follows SuperTrend:** Accuracy > 50% (reliable signals)
- **Moderate:** 30% ≤ Accuracy ≤ 50% (mixed signals)
- **Does NOT Follow:** Accuracy < 30% (unreliable signals)

### 7. Visualization
- Power BI dashboard for sector performance and signal distribution
- Interactive charts showing accuracy by industry
- Trade-level details for validation

---

## 📈 Backtesting Results

### Overall Performance (10,2 Parameters)

**Dataset:** 545 NIFTY 500 stocks, 2015-2024

| Metric | Value |
|--------|-------|
| **Total Stocks Analyzed** | 545 |
| **Average Signal Accuracy** | 41.58% |
| **Median Signal Accuracy** | 40.00% |
| **Median Annual Return** | 10.42% |
| **Average Trades/Stock** | 6.89 |
| **Average Holding Period** | 144 days |

### Signal Classification

| Category | Count | Percentage |
|----------|-------|-----------|
| Follows SuperTrend | 143 | 26.2% |
| Moderate | 214 | 39.3% |
| Does NOT Follow | 188 | 34.5% |

### Distribution of Returns

| Return Range | Stock Count |
|-------------|------------|
| \> 50% | ~18 |
| 10-50% | ~85 |
| 0-10% | ~118 |
| -10 to 0% | ~142 |
| < -10% | ~182 |

(Many stocks returned NaN due to lack of trades or insufficient data)

---

## 🎯 Parameter Comparison: (7,1) vs (10,2)

### Comparative Analysis

| Metric | (7,1) Aggressive | (10,2) Conservative |
|--------|------------------|-------------------|
| **Stocks Analyzed** | 1,962 | 545 |
| **Avg Accuracy** | 39.19% | 41.58% |
| **Median Return** | 16.89% | 10.42% |
| **Avg Trades/Stock** | (varies) | 6.89 |
| **Category: Follows** | 484 (24.7%) | 143 (26.2%) |
| **Category: Moderate** | 920 (46.9%) | 214 (39.3%) |
| **Category: Does NOT Follow** | 558 (28.4%) | 188 (34.5%) |

### Observations
1. **10,2 Parameters:** Slightly higher average accuracy (41.58% vs 39.19%)
2. **7,1 Parameters:** Applied to more stocks, higher median return but wider variance
3. Trade-off between consistency (10,2) and signal frequency (7,1)
4. Both configurations show modest signal accuracy (below 50%)

---

## 🏭 Sector-wise Performance (10,2 Parameters)

### Top Performing Sectors

| Sector | Accuracy | Avg Return | Stocks |
|--------|----------|-----------|--------|
| Automobile & Auto Components | 55.24% | +0.17 | 7 |
| Capital Goods | 53.49% | +0.32 | 17 |
| Oil Gas & Consumable Fuels | 51.87% | +0.19 | 10 |
| Consumer Durables | 47.12% | +0.18 | 7 |
| Metals & Mining | 46.24% | +0.18 | 11 |

### Moderate Performing Sectors

| Sector | Accuracy | Avg Return | Stocks |
|--------|----------|-----------|--------|
| Financial Services | 45.88% | +0.15 | 47 |
| Realty | 43.43% | +0.17 | 5 |
| Information Technology | 41.83% | +0.05 | 11 |

### Challenging Sectors

| Sector | Accuracy | Avg Return | Stocks |
|--------|----------|-----------|--------|
| Consumer Services | 32.98% | +0.09 | 6 |
| Construction Materials | 36.11% | -0.04 | 3 |
| Media & Entertainment | 28.57% | -0.33 | 1 |
| Textiles | 14.29% | -0.65 | 1 |

**Key Insight:** SuperTrend effectiveness varies significantly by sector. Capital-intensive sectors (Auto, Capital Goods) show stronger signals than discretionary/volatile sectors (Textiles, Media).

---

## 📊 Dashboard & Visualization

### Power BI Dashboard

![SuperTrend Strategy Analysis Dashboard](6_dashboard/dashboard_1.png)

**Dashboard Components:**

1. **Industry-wise Performance**
   - Visualization: Sector accuracy and average returns
   - Data: Grouped by NIFTY 500 industry classification
   - Purpose: Identify sectors best suited for SuperTrend strategy

2. **Accuracy Distribution**
   - Visualization: Performance by sector with accuracy benchmarks
   - Data: Signal accuracy % by industry
   - Purpose: Compare sector-specific signal reliability

3. **Effectiveness Breakdown**
   - Visualization: Pie chart showing signal category distribution
   - Data: Percentage of stocks in each category
   - Purpose: Quick overview of overall signal quality

**Data Connection:** Reads from PostgreSQL `stock_market_analysis` schema

---

## 💡 Key Findings & Observations

### Finding 1: Sector Dependency
SuperTrend effectiveness is **highly sector-dependent**. Capital-intensive sectors (Automobile, Capital Goods) show 50%+ accuracy, while cyclical sectors (Textiles, Media) show <30% accuracy. This suggests the indicator works better for stable, trending businesses.

### Finding 2: Parameter Impact on Signal Generation
- **(10,2):** More restrictive bands → fewer trades, slightly higher accuracy (41.58%)
- **(7,1):** Tighter bands → more trades, lower accuracy (39.19%)
- Both achieve ~40% average accuracy, indicating parameter choice affects frequency not quality

### Finding 3: Low Absolute Accuracy Rates
Average accuracy of 41.58% across all stocks suggests **SuperTrend alone is insufficient for reliable trading**. Results are only marginally better than random chance (50%).

### Finding 4: Holding Period Distribution
Average holding period of 144 days suggests the indicator captures multi-month trends rather than short-term moves.

### Finding 5: Missing Returns Data
Many stocks show NaN (not a number) values for returns, indicating insufficient trades were generated to evaluate performance meaningfully.

---

## ⚠️ Limitations & Disclaimers

### Backtesting Limitations
1. **Historical Data Only** - No live validation or forward-testing
2. **No Transaction Costs** - Excludes brokerage, taxes, market impact
3. **No Slippage Modeling** - Assumes execution at signal price (unrealistic)
4. **Weekly Data** - Aggregates intraday volatility, may miss intraday signals
5. **Survivorship Bias** - Uses NIFTY 500 list as of 2024 (some stocks didn't exist in 2015)

### Indicator Limitations
1. **Single Indicator** - No use of volume, momentum, or other confirmations
2. **No Market Regime Detection** - Same parameters across bull/bear/sideways markets
3. **Parameter Sensitivity** - Results highly dependent on length and factor choices
4. **Lag Effect** - ATR/bands are backward-looking, may miss trend starts

### Data Limitations
1. **Adjusted vs Unadjusted Prices** - Yahoo Finance adjusts for splits/dividends
2. **Corporate Actions** - Doesn't account for bonus/rights separately
3. **Delisted Stocks** - May exclude stocks delisted during period
4. **Price Gaps** - Doesn't model opening gaps or limit-up/limit-down moves

### Analysis Limitations
1. **No Walk-Forward Validation** - Single backtest, no time-series cross-validation
2. **No Out-of-Sample Testing** - Parameters optimized on same data used for testing
3. **No Machine Learning** - Parameters chosen manually, not optimized statistically
4. **Small Sample Sizes** - Some sectors have <10 stocks, results may not be statistically significant

---

## 🚀 Future Enhancements

### Signal Confirmation Methods
- [ ] Combine with RSI for overbought/oversold states
- [ ] Add volume confirmation (price + volume trend alignment)
- [ ] Implement MACD confirmation
- [ ] Use moving average crossovers as additional filters

---

##  License

MIT License - See [LICENSE](LICENSE) for details

## ⚠️ Disclaimer

This project is **for educational and research purposes only**. Historical backtesting does not guarantee future performance. The SuperTrend indicator should not be used as the sole basis for investment decisions. Always consult financial advisors and conduct thorough due diligence before trading.

---

**Last Updated:** June 19, 2026  
**Analysis Period:** 2015-2024 (10 years of data)  
**Stocks Analyzed:** 545 with (10,2), 1,962 with (7,1) parameters  
**Status:** ✅ Backtesting Complete
