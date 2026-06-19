import pandas as pd
import psycopg2

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
    if df["Close"].iloc[i] > df["UPPER"].iloc[i-1]:
        trend = True
    elif df["Close"].iloc[i] < df["LOWER"].iloc[i-1]:
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
    if df["Close"].iloc[i] > df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] <= df["SuperTrend"].iloc[i-1]:
        df.iloc[i, df.columns.get_loc("Signal")] = "BUY"

    elif df["Close"].iloc[i] < df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] >= df["SuperTrend"].iloc[i-1]:
        df.iloc[i, df.columns.get_loc("Signal")] = "SELL"

# -------------------------------
# PRINT SIGNALS
# -------------------------------
signals = df[df["Signal"] != ""]
print("\n📊 SIGNALS:\n", signals[["Close", "SuperTrend", "Signal"]])

# -------------------------------
# TRADES
# -------------------------------
# trades = []

# in_trade = False
# entry_price = 0
# entry_date = None

# for i in range(len(df)):
#     signal = df["Signal"].iloc[i]

#     if signal == "BUY" and not in_trade:
#         in_trade = True
#         entry_price = df["Close"].iloc[i]
#         entry_date = df.index[i]

#     elif signal == "SELL" and in_trade:
#         exit_price = df["Close"].iloc[i]
#         exit_date = df.index[i]

#         ret = (exit_price - entry_price) / entry_price
#         holding_days = (exit_date - entry_date).days

#         trades.append({
#             "Entry_Date": entry_date,
#             "Exit_Date": exit_date,
#             "Return": ret,
#             "Holding_Days": holding_days
#         })

#         in_trade = False


trades = []

in_trade = False
entry_price = 0
entry_date = None

for i in range(len(df)):

    price = df["Close"].iloc[i]
    signal = df["Signal"].iloc[i]

    # ENTRY
    if signal == "BUY" and not in_trade:
        in_trade = True
        entry_price = price
        entry_date = df.index[i]

    # EXIT CONDITIONS
    elif in_trade:

        current_return = (price - entry_price) / entry_price

        exit_flag = False

        # 1. SELL signal
        if signal == "SELL":
            exit_flag = True

        # 2. Profit booking (5%)
        elif current_return >= 0.05:
            exit_flag = True

        # 3. Stop loss (-3%)
        elif current_return <= -0.03:
            exit_flag = True

        if exit_flag:
            exit_price = price
            exit_date = df.index[i]

            holding_days = (exit_date - entry_date).days

            trades.append({
                "Entry_Date": entry_date,
                "Exit_Date": exit_date,
                "Return": current_return,
                "Holding_Days": holding_days
            })

            in_trade = False

trades_df = pd.DataFrame(trades)

print("\n📈 TRADES:\n", trades_df)

# -------------------------------
# SUMMARY
# -------------------------------
if trades_df.empty:
    print("\n❌ No trades generated")
else:
    total_return = trades_df["Return"].sum()
    num_trades = len(trades_df)
    accuracy = (trades_df["Return"] > 0).mean() * 100

    total_days = trades_df["Holding_Days"].sum()

    if total_days > 0:
        annual_return = (1 + total_return) ** (365 / total_days) - 1
    else:
        annual_return = 0

    print("\n📊 SUMMARY:")
    print(f"Total Return: {total_return:.2f}")
    print(f"Trades: {num_trades}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Annual Return: {annual_return:.2f}")

# -------------------------------
# SIGNAL ACCURACY (NEW 🔥)
# -------------------------------
correct = 0
total = 0

for i in range(len(df) - 5):   # next 5 days check
    if df["Signal"].iloc[i] == "BUY":
        total += 1
        if df["Close"].iloc[i + 5] > df["Close"].iloc[i]:
            correct += 1

if total > 0:
    signal_accuracy = (correct / total) * 100
else:
    signal_accuracy = 0

print(f"\n🎯 Signal Accuracy (5-day): {signal_accuracy:.2f}%")

# import pandas as pd
# import psycopg2

# # STEP 1: Connect
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="postgres",
#     host="localhost",
#     port="5432"
# )

# # STEP 2: Fetch data
# query = """
# SELECT trade_date, high_price, low_price, close_price
# FROM stock_market_analysis.nse_trade_daily
# WHERE symbol = 'RELIANCE'
# AND trade_date >= '2021-01-01'
# ORDER BY trade_date
# """

# df = pd.read_sql(query, conn)

# # STEP 3: Prepare
# df["trade_date"] = pd.to_datetime(df["trade_date"])
# df.set_index("trade_date", inplace=True)

# df.rename(columns={
#     "high_price": "High",
#     "low_price": "Low",
#     "close_price": "Close"
# }, inplace=True)

# # 🔥 STEP 4: Convert to WEEKLY
# df = df.resample("W").agg({
#     "High": "max",
#     "Low": "min",
#     "Close": "last"
# }).dropna()

# # STEP 5: Parameters (changed)
# length = 7
# factor = 1

# # STEP 6: ATR
# df["H-L"] = df["High"] - df["Low"]
# df["H-PC"] = abs(df["High"] - df["Close"].shift(1))
# df["L-PC"] = abs(df["Low"] - df["Close"].shift(1))

# df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
# df["ATR"] = df["TR"].rolling(length).mean()

# # STEP 7: Bands
# df["MID"] = (df["High"] + df["Low"]) / 2
# df["UPPER"] = df["MID"] + factor * df["ATR"]
# df["LOWER"] = df["MID"] - factor * df["ATR"]

# # STEP 8: SuperTrend
# df["SuperTrend"] = 0.0
# trend = True

# for i in range(1, len(df)):
#     if df["Close"].iloc[i] > df["UPPER"].iloc[i-1]:
#         trend = True
#     elif df["Close"].iloc[i] < df["LOWER"].iloc[i-1]:
#         trend = False

#     if trend:
#         df.iloc[i, df.columns.get_loc("SuperTrend")] = df["LOWER"].iloc[i]
#     else:
#         df.iloc[i, df.columns.get_loc("SuperTrend")] = df["UPPER"].iloc[i]

# # STEP 9: Signals
# df["Signal"] = ""

# for i in range(1, len(df)):
#     if df["Close"].iloc[i] > df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] <= df["SuperTrend"].iloc[i-1]:
#         df.iloc[i, df.columns.get_loc("Signal")] = "BUY"

#     elif df["Close"].iloc[i] < df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] >= df["SuperTrend"].iloc[i-1]:
#         df.iloc[i, df.columns.get_loc("Signal")] = "SELL"

# # CHECK SIGNALS
# print(df[df["Signal"] != ""])

# # ---- TRADES ----
# trades = []

# in_trade = False
# entry_price = 0
# entry_date = None

# for i in range(len(df)):
#     signal = df["Signal"].iloc[i]

#     if signal == "BUY" and not in_trade:
#         in_trade = True
#         entry_price = df["Close"].iloc[i]
#         entry_date = df.index[i]

#     elif signal == "SELL" and in_trade:
#         exit_price = df["Close"].iloc[i]
#         exit_date = df.index[i]

#         ret = (exit_price - entry_price) / entry_price

#         trades.append({
#             "Symbol": "TCS",
#             "Entry_Date": entry_date,
#             "Exit_Date": exit_date,
#             "Entry_Price": entry_price,
#             "Exit_Price": exit_price,
#             "Return": ret
#         })

#         in_trade = False

# trades_df = pd.DataFrame(trades)

# print(trades_df)


# # ---- SUMMARY ----

# total_return = trades_df["Return"].sum()
# avg_return = trades_df["Return"].mean()
# num_trades = len(trades_df)
# accuracy = (trades_df["Return"] > 0).mean() * 100

# summary = {
#     "Symbol": "TCS",
#     "Total_Return": total_return,
#     "Avg_Return": avg_return,
#     "Trades": num_trades,
#     "Accuracy": accuracy
# }

# summary_df = pd.DataFrame([summary])

# print(summary_df)