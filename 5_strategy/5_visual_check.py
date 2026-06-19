import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# -------------------------------
# CONNECT DB
# -------------------------------
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# -------------------------------
# STOCK SELECTION
# -------------------------------
symbol = "RELIANCE"

query = f"""
SELECT trade_date, high_price, low_price, close_price
FROM stock_market_analysis.nse_trade_daily
WHERE symbol = '{symbol}'
AND trade_date >= '2021-01-01'
ORDER BY trade_date
"""

df = pd.read_sql(query, conn)

# -------------------------------
# PREPARE DATA
# -------------------------------
df["trade_date"] = pd.to_datetime(df["trade_date"])
df.set_index("trade_date", inplace=True)

df.rename(columns={
    "high_price": "High",
    "low_price": "Low",
    "close_price": "Close"
}, inplace=True)

# -------------------------------
# PARAMETERS
# -------------------------------
length = 10
factor = 2

# -------------------------------
# ATR
# -------------------------------
df["H-L"] = df["High"] - df["Low"]
df["H-PC"] = abs(df["High"] - df["Close"].shift(1))
df["L-PC"] = abs(df["Low"] - df["Close"].shift(1))

df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
df["ATR"] = df["TR"].rolling(length).mean()

# -------------------------------
# BANDS
# -------------------------------
df["MID"] = (df["High"] + df["Low"]) / 2

df["UPPER"] = df["MID"] + factor * df["ATR"]
df["LOWER"] = df["MID"] - factor * df["ATR"]

# -------------------------------
# SUPERTREND
# -------------------------------
df["SuperTrend"] = 0.0

trend = True

for i in range(1, len(df)):

    if df["Close"].iloc[i] > df["UPPER"].iloc[i - 1]:
        trend = True

    elif df["Close"].iloc[i] < df["LOWER"].iloc[i - 1]:
        trend = False

    if trend:
        df.iloc[i, df.columns.get_loc("SuperTrend")] = df["LOWER"].iloc[i]

    else:
        df.iloc[i, df.columns.get_loc("SuperTrend")] = df["UPPER"].iloc[i]

# -------------------------------
# SIGNALS
# -------------------------------
df["Signal"] = ""

for i in range(1, len(df)):

    # BUY
    if (
        df["Close"].iloc[i] > df["SuperTrend"].iloc[i]
        and
        df["Close"].iloc[i - 1] <= df["SuperTrend"].iloc[i - 1]
    ):

        df.iloc[i, df.columns.get_loc("Signal")] = "BUY"

    # SELL
    elif (
        df["Close"].iloc[i] < df["SuperTrend"].iloc[i]
        and
        df["Close"].iloc[i - 1] >= df["SuperTrend"].iloc[i - 1]
    ):

        df.iloc[i, df.columns.get_loc("Signal")] = "SELL"

# -------------------------------
# SIGNAL DATA
# -------------------------------
buy_signals = df[df["Signal"] == "BUY"]
sell_signals = df[df["Signal"] == "SELL"]

# -------------------------------
# VISUAL CHECK
# -------------------------------
plt.figure(figsize=(16, 8))

# Close Price
plt.plot(
    df.index,
    df["Close"],
    label="Close Price"
)

# SuperTrend
plt.plot(
    df.index,
    df["SuperTrend"],
    label="SuperTrend"
)

# BUY Signals
plt.scatter(
    buy_signals.index,
    buy_signals["Close"],
    marker="^",
    s=100,
    label="BUY"
)

# SELL Signals
plt.scatter(
    sell_signals.index,
    sell_signals["Close"],
    marker="v",
    s=100,
    label="SELL"
)

plt.title(f"{symbol} SuperTrend Verification")

plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.grid(True)

plt.show()