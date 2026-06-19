import pandas as pd
import yfinance as yf
import time

# STEP 1: Load weekly data
df = pd.read_csv("../data/securities/weekly_prices.csv")

# STEP 2: Get unique stocks
symbols = df["Symbol"].unique()

mktcap_data = []

# STEP 3: Fetch market cap (accurate approach)
for sym in symbols:
    print("Fetching Market Cap:", sym)

    try:
        ticker = sym + ".NS"
        info = yf.Ticker(ticker).info

        shares = info.get("sharesOutstanding", None)

        if shares:
            mktcap_data.append([sym, shares])

    except:
        continue

    time.sleep(0.5)

# STEP 4: Create DataFrame
shares_df = pd.DataFrame(mktcap_data, columns=["Symbol", "Shares"])

# STEP 5: Merge shares with price data
merged = df.merge(shares_df, on="Symbol")

# STEP 6: Compute Market Cap dynamically
merged["MarketCap"] = merged["Shares"] * merged["Close"]

# STEP 7: Sector total market cap
merged["sector_mktcap"] = merged.groupby(
    ["Date", "Industry"]
)["MarketCap"].transform("sum")

# STEP 8: Compute weights
merged["weight"] = merged["MarketCap"] / merged["sector_mktcap"]

# STEP 9: Weighted return
merged["weighted_return"] = merged["Return"] * merged["weight"]

# STEP 10: Sector returns
sector_returns = merged.groupby(
    ["Date", "Industry"]
)["weighted_return"].sum().reset_index()

sector_returns.columns = ["Date", "Sector", "Sector_Return"]

# STEP 11: Save final output
sector_returns.to_csv("../data/securities/sector_returns.csv", index=False)

print("✅ FINAL OUTPUT CREATED — sector_returns.csv")