import pandas as pd
import yfinance as yf

# STEP 1: Load NSE Nifty 500 file
stocks = pd.read_csv("../data/securities/nifty500.csv")

# STEP 2: Prepare tickers
tickers = stocks["Symbol"].tolist()
tickers = [t + ".NS" for t in tickers]

# STEP 3: Function to get weekly data
def get_weekly_prices(ticker):
    try:
        df = yf.download(
            ticker,
            start="2015-01-01",
            end="2024-12-31",
            interval="1wk",
            progress=False
        )

        # ❌ skip if no data
        if df.empty:
            return None

        # ✅ fix multi-level columns
        df.columns = df.columns.get_level_values(0)

        df = df[["Open", "Close"]]
        df["Return"] = (df["Close"] - df["Open"]) / df["Open"]
        df["Symbol"] = ticker.replace(".NS", "")

        return df.reset_index()

    except:
        return None


# STEP 4: Fetch data safely
data_list = []

for t in tickers:
    print("Processing:", t)

    df = get_weekly_prices(t)
    if df is not None:
        data_list.append(df)

# Combine all
all_data = pd.concat(data_list)

# STEP 5: Merge with sector (Industry)
merged = all_data.merge(
    stocks[["Symbol", "Industry"]],
    on="Symbol"
)

# STEP 6: Accuracy checks
print("Total stocks in NSE file:", len(stocks))
print("Stocks after processing:", merged["Symbol"].nunique())

missing = set(stocks["Symbol"]) - set(merged["Symbol"])
print("Missing stocks count:", len(missing))

# STEP 7: Save file
merged.to_csv("../data/securities/weekly_prices.csv", index=False)

print("✅ FINAL DATA CREATED — weekly_prices.csv")