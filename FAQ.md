# FAQ - Frequently Asked Questions

## General Questions

### Q: What is this project about?
A: This is a comprehensive technical analysis project implementing the SuperTrend indicator on 500+ Indian stocks. It analyzes 25+ years of historical data to backtest trend-following strategies and identify sector-wise performance patterns.

### Q: Who should use this?
A: 
- Technical analysts interested in trend-following strategies
- Traders looking for systematic entry/exit signals
- Researchers studying market behavior and indicators
- Students learning technical analysis implementation
- Anyone interested in Indian stock market analysis

### Q: Is this for live trading?
A: This project provides analysis and backtesting results. It's designed for paper trading first. Users must implement their own risk management, testing, and live trading integration before using real capital.

### Q: What data does this analyze?
A: 
- 500+ Indian stocks from NSE (National Stock Exchange)
- 5,000+ stocks from BSE (Bombay Stock Exchange)
- 25+ years of historical data (2001-2026)
- Block deals and bulk deals data
- Sector classification and performance metrics

---

## Installation & Setup

### Q: What are the prerequisites?
A: You'll need:
- Python 3.8 or higher
- PostgreSQL 12 or higher
- 2GB+ disk space for data
- Internet connection for data fetching
- Power BI Desktop (optional, for dashboard)

### Q: How do I install the dependencies?
A: 
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Q: I'm getting a TA-Lib installation error. How to fix?
A:
```bash
# Try installing from wheels first
pip install TA-Lib --no-cache-dir

# If that fails, install from source
# On Windows: Download binary wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/
# On Mac: brew install ta-lib
# On Linux: apt-get install ta-lib
```

### Q: How do I set up the PostgreSQL database?
A: 
```bash
# Create database
createdb stock_analysis

# Update connection in 2_loading/ scripts
# Default: localhost, postgres user, stock_analysis database
```

---

## Data & Analysis

### Q: How do I fetch the latest price data?
A:
```bash
python 1_collection/fetch_prices.py
```

### Q: Where is the data stored?
A:
- **CSV Files:** `nse_history_csv/` and `bse_history_csv/`
- **Database:** PostgreSQL tables
  - `nse_trade_daily` (NSE prices)
  - `bse_trade_daily` (BSE prices)
  - `sec_master` (Securities reference)

### Q: How often is data updated?
A: Daily updates run automatically via:
```bash
python 3_daily_updates/run_daily_update.py
```

### Q: Can I analyze other markets?
A: Currently configured for NSE/BSE. To extend:
1. Modify fetch scripts to include other sources
2. Update database schema for new data
3. Adjust sector classification
4. Update analysis scripts

---

## SuperTrend Strategy

### Q: What are the two parameter configurations?
A:
- **(7,1) Aggressive:** More trades, lower accuracy, faster signals
- **(10,2) Conservative:** Fewer trades, higher accuracy (56%), slower signals

### Q: Which parameters should I use?
A: 
- Start with (10,2) for reliability
- Try (7,1) only if you're an active trader
- Adjust based on your sector and risk tolerance

### Q: What's the difference between accuracy and win rate?
A:
- **Accuracy:** Percentage of correct signals overall
- **Win Rate:** Percentage of profitable trades among executed signals

### Q: How do I generate signals for a specific stock?
A:
```python
# In 5_strategy/1_supertrend_signals.py
python -c "python 1_supertrend_signals.py --symbol INFY --sector IT"
```

---

## Performance & Results

### Q: What returns can I expect?
A:
- **Conservative:** 15-25% annual (following all guidelines)
- **Favorable:** 30-45% in bull markets
- **Pessimistic:** 5-10% or negative in difficult conditions

### Q: Which sectors perform best?
A:
1. Automobile & Auto Components (55% accuracy)
2. Capital Goods (52% accuracy, +0.32% returns)
3. Oil & Gas (52% accuracy)
4. Consumer Durables (50% accuracy)
5. Metals & Mining (48% accuracy)

### Q: Which sectors should I avoid?
A:
- Textiles (14% accuracy, -0.65% returns)
- Media & Entertainment (29% accuracy, -0.33%)
- Construction Materials (low accuracy)

### Q: How accurate are the backtesting results?
A: 
- Results assume no slippage or fees
- Live trading will differ due to:
  - Execution slippage
  - Trading costs and taxes
  - Market liquidity
  - Psychological factors

---

## Dashboard & Visualization

### Q: How do I view the Power BI dashboard?
A:
1. Install Power BI Desktop
2. Open: `6_dashboard/power_bi_supertrend_01.pbix`
3. Click "Refresh" to load latest data

### Q: Dashboard shows old data. What do I do?
A:
1. Verify data updates completed (check 3_daily_updates/)
2. Refresh in Power BI (F5)
3. Clear Power BI cache if needed
4. Verify database connection

### Q: Can I modify the dashboard?
A: Yes, open in Power BI Desktop and edit:
- Add new visualizations
- Change colors and formatting
- Create custom measures
- Publish to Power BI Service

### Q: Can I use different visualization tools?
A: Yes, you can:
- Query PostgreSQL directly
- Use Tableau, Qlik, or other tools
- Create custom Python visualizations
- Export data to CSV for analysis

---

## Risk Management

### Q: What stop-loss should I use?
A: Recommended: -15% below entry price
- This balances protection vs false breakouts
- Adjust based on volatility and sector
- Monitor average adverse excursion

### Q: What position size should I use?
A:
- Risk 2-3% per trade maximum
- Use ATR for position sizing
- Diversify across sectors
- Monitor portfolio concentration

### Q: How do I manage drawdowns?
A:
1. Use hard stop-losses
2. Limit position sizing
3. Monitor volatility regime
4. Disable during consolidation periods
5. Track max drawdown continuously

### Q: Should I combine with other indicators?
A: Yes, consider:
- RSI for overbought/oversold confirmation
- Volume for signal strength
- Moving averages for trend context
- Support/resistance levels

---

## Troubleshooting

### Q: Data collection fails with timeout error
A:
- Check internet connection
- Verify yfinance is working
- Try running individually for each stock
- Check rate limiting

### Q: PostgreSQL connection error
A:
- Verify PostgreSQL is running
- Check credentials in config
- Ensure database exists
- Check network connectivity

### Q: Low accuracy on certain sectors
A:
- Review parameter settings
- Check if sector is in "avoid" list
- Verify data quality
- Consider additional filters

### Q: Dashboard won't refresh
A:
- Check database connection
- Verify data was loaded
- Restart Power BI
- Clear cache: `C:\Users\USERNAME\AppData\Local\Microsoft\Power BI Desktop`

### Q: Slow performance on large queries
A:
- Check database indexes
- Consider data partitioning
- Limit historical lookback period
- Upgrade database resources

---

## Advanced Usage

### Q: How do I modify the analysis period?
A: In strategy scripts, adjust:
```python
START_DATE = "2021-01-01"  # Change start date
END_DATE = "2026-03-23"    # Change end date
```

### Q: Can I add new sectors?
A:
1. Update sector classification in `sec_master` table
2. Modify 4_eda/ sector analysis
3. Update 6_dashboard/ visualizations
4. Re-run strategy analysis

### Q: How do I implement live trading?
A:
1. Set up paper trading first (TradingView, broker platform)
2. Verify signals match your system
3. Implement position management logic
4. Add risk controls and monitoring
5. Start with small positions
6. Scale gradually after verification

### Q: Can I run this on the cloud?
A: Yes, options include:
- AWS RDS for PostgreSQL
- Google Cloud SQL
- Heroku for Python scripts
- Azure for full stack
- DigitalOcean for simple setup

---

## Contributing

### Q: How do I contribute to this project?
A: See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Reporting bugs
- Suggesting features
- Submitting code
- Code style requirements

### Q: I found a bug. What should I do?
A:
1. Check if it's already reported in Issues
2. Create new Issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python/OS version, database version

### Q: Can I fork and modify for my own use?
A: Yes! This is MIT licensed. You can:
- Fork the repository
- Modify for personal use
- Share improvements (appreciated but optional)
- Credit original project

---

## Performance Optimization

### Q: How do I make the analysis run faster?
A:
1. Use database indexes (already configured)
2. Limit lookback period
3. Filter to specific sectors
4. Run analysis in parallel for multiple stocks
5. Use a more powerful machine

### Q: How much disk space do I need?
A:
- CSV files: ~500MB
- PostgreSQL database: ~1GB
- Power BI cache: ~100MB
- Total: ~2GB minimum

### Q: Can I run this on a Raspberry Pi?
A: Not recommended due to:
- Memory constraints (4GB max typical)
- Processing power for large calculations
- Database performance limitations
- Better to use cloud infrastructure

---

## Licensing & Legal

### Q: What's the license?
A: MIT License - see [LICENSE](LICENSE)
- Free to use, modify, distribute
- Must include license and copyright notice
- No warranty or liability

### Q: Can I use this for commercial trading?
A: Legally yes, but:
- Consult financial advisor first
- Test extensively before risking capital
- This analysis is NOT financial advice
- You assume all trading risks
- Comply with local regulations

### Q: What are the disclaimers?
A:
- Past performance ≠ future results
- Backtesting ≠ live trading performance
- Strategy requires active monitoring
- Not suitable for all traders
- Test on paper trading first

---

## Getting Help

### Q: Where do I find more information?
A:
- **Detailed Guide:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Quick Start:** [README.md](README.md)
- **Contribution Guide:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Change History:** [CHANGELOG.md](CHANGELOG.md)

### Q: Who can I contact with questions?
A:
- GitHub Issues for bugs/features
- GitHub Discussions for questions
- Check FAQ first (this document)
- Review existing documentation

### Q: How do I report security issues?
A: Don't post in Issues if security-related
- Email directly to project maintainers
- Include reproduction steps
- Allow time for fix before disclosure

---

**Last Updated:** June 19, 2026  
**Status:** ✅ Complete

Need more help? See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed information.
