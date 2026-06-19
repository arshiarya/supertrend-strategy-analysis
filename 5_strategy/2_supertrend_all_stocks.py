# import pandas as pd
# import psycopg2

# # -------------------------------
# # CONNECT DB
# # -------------------------------
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="postgres",
#     host="localhost",
#     port="5432"
# )

# # -------------------------------
# # GET ALL SYMBOLS
# # -------------------------------
# symbols_query = """
# SELECT DISTINCT symbol
# FROM stock_market_analysis.nse_trade_daily
# """

# symbols = pd.read_sql(symbols_query, conn)["symbol"].tolist()

# print(f"Total stocks: {len(symbols)}")

# # -------------------------------
# # PARAMETERS (FINAL CHOICE)
# # -------------------------------
# length = 7
# factor = 1

# all_trades = []
# all_summary = []

# # -------------------------------
# # LOOP THROUGH ALL STOCKS
# # -------------------------------
# for symbol in symbols:

#     try:
#         print(f"Processing: {symbol}")

#         query = f"""
#         SELECT trade_date, high_price, low_price, close_price
#         FROM stock_market_analysis.nse_trade_daily
#         WHERE symbol = '{symbol}'
#         AND trade_date >= '2021-01-01'
#         ORDER BY trade_date
#         """

#         df = pd.read_sql(query, conn)

#         if df.empty:
#             continue

#         # -------------------------------
#         # PREPARE DATA
#         # -------------------------------
#         df["trade_date"] = pd.to_datetime(df["trade_date"])
#         df.set_index("trade_date", inplace=True)

#         df.rename(columns={
#             "high_price": "High",
#             "low_price": "Low",
#             "close_price": "Close"
#         }, inplace=True)

#         # -------------------------------
#         # ATR
#         # -------------------------------
#         df["H-L"] = df["High"] - df["Low"]
#         df["H-PC"] = abs(df["High"] - df["Close"].shift(1))
#         df["L-PC"] = abs(df["Low"] - df["Close"].shift(1))

#         df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
#         df["ATR"] = df["TR"].rolling(length).mean()

#         # -------------------------------
#         # BANDS
#         # -------------------------------
#         df["MID"] = (df["High"] + df["Low"]) / 2
#         df["UPPER"] = df["MID"] + factor * df["ATR"]
#         df["LOWER"] = df["MID"] - factor * df["ATR"]

#         # -------------------------------
#         # SUPERTREND
#         # -------------------------------
#         df["SuperTrend"] = 0.0
#         trend = True

#         for i in range(1, len(df)):
#             if df["Close"].iloc[i] > df["UPPER"].iloc[i-1]:
#                 trend = True
#             elif df["Close"].iloc[i] < df["LOWER"].iloc[i-1]:
#                 trend = False

#             if trend:
#                 df.iloc[i, df.columns.get_loc("SuperTrend")] = df["LOWER"].iloc[i]
#             else:
#                 df.iloc[i, df.columns.get_loc("SuperTrend")] = df["UPPER"].iloc[i]

#         # -------------------------------
#         # SIGNALS
#         # -------------------------------
#         df["Signal"] = ""

#         for i in range(1, len(df)):
#             if df["Close"].iloc[i] > df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] <= df["SuperTrend"].iloc[i-1]:
#                 df.iloc[i, df.columns.get_loc("Signal")] = "BUY"

#             elif df["Close"].iloc[i] < df["SuperTrend"].iloc[i] and df["Close"].iloc[i-1] >= df["SuperTrend"].iloc[i-1]:
#                 df.iloc[i, df.columns.get_loc("Signal")] = "SELL"

#         # -------------------------------
#         # TRADES
#         # -------------------------------
#         trades = []

#         in_trade = False
#         entry_price = 0
#         entry_date = None

#         for i in range(len(df)):
#             signal = df["Signal"].iloc[i]

#             if signal == "BUY" and not in_trade:
#                 in_trade = True
#                 entry_price = df["Close"].iloc[i]
#                 entry_date = df.index[i]

#             elif signal == "SELL" and in_trade:
#                 exit_price = df["Close"].iloc[i]
#                 exit_date = df.index[i]

#                 ret = (exit_price - entry_price) / entry_price
#                 holding_days = (exit_date - entry_date).days

#                 if holding_days > 0:
#                     monthly_return = (ret / holding_days) * 30
#                 else:
#                     monthly_return = 0

#                 trades.append({
#                     "Symbol": symbol,
#                     "Entry_Date": entry_date,
#                     "Exit_Date": exit_date,
#                     "Entry_Price": entry_price,
#                     "Exit_Price": exit_price,
#                     "Return": ret,
#                     "Holding_Days": holding_days,
#                     "Monthly_Return": monthly_return
#                 })

#                 in_trade = False

#         trades_df = pd.DataFrame(trades)

#         # -------------------------------
#         # SAVE TRADES
#         # -------------------------------
#         if not trades_df.empty:
#             all_trades.append(trades_df)

#             total_return = trades_df["Return"].sum()
#             avg_return = trades_df["Return"].mean()
#             num_trades = len(trades_df)
#             accuracy = (trades_df["Return"] > 0).mean() * 100

#             total_days = trades_df["Holding_Days"].sum()
#             avg_holding = trades_df["Holding_Days"].mean()

#             if total_days > 0:
#                 annual_return = (1 + total_return) ** (365 / total_days) - 1
#             else:
#                 annual_return = 0

#             avg_monthly_return = trades_df["Monthly_Return"].mean()

#         else:
#             total_return = 0
#             avg_return = 0
#             num_trades = 0
#             accuracy = 0
#             avg_holding = 0
#             annual_return = 0
#             avg_monthly_return = 0

#         all_summary.append({
#             "Symbol": symbol,
#             "Total_Return": total_return,
#             "Avg_Return": avg_return,
#             "Trades": num_trades,
#             "Accuracy": accuracy,
#             "Avg_Holding_Days": avg_holding,
#             "Annual_Return": annual_return,
#             "Avg_Monthly_Return": avg_monthly_return
#         })

#     except Exception as e:
#         print(f"Error in {symbol}: {e}")
#         continue

# # -------------------------------
# # FINAL OUTPUT
# # -------------------------------
# final_trades = pd.concat(all_trades, ignore_index=True)
# final_summary = pd.DataFrame(all_summary)

# # SAVE FILES
# final_trades.to_csv("../data/securities/all_trades.csv", index=False)
# final_summary.to_csv("../data/securities/summary_7_1.csv", index=False)

# print("\n✅ DONE — Files Created")



import pandas as pd
import psycopg2
import math

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
# GET ALL SYMBOLS
# -------------------------------
symbols_query = """
SELECT DISTINCT symbol
FROM stock_market_analysis.nse_trade_daily
"""

symbols = pd.read_sql(symbols_query, conn)["symbol"].tolist()

print(f"Total stocks: {len(symbols)}")

# -------------------------------
# PARAMETERS
# -------------------------------
length = 10
factor = 2

all_summary = []

# -------------------------------
# LOOP THROUGH STOCKS
# -------------------------------
for symbol in symbols:

    try:
        print(f"Processing: {symbol}")

        query = f"""
        SELECT trade_date, high_price, low_price, close_price
        FROM stock_market_analysis.nse_trade_daily
        WHERE symbol = '{symbol}'
        AND trade_date >= '2021-01-01'
        ORDER BY trade_date
        """

        df = pd.read_sql(query, conn)

        if df.empty:
            continue

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
        # TRADES
        # -------------------------------
        trades = []

        in_trade = False
        entry_price = 0
        entry_date = None

        for i in range(len(df)):
            signal = df["Signal"].iloc[i]

            if signal == "BUY" and not in_trade:
                in_trade = True
                entry_price = df["Close"].iloc[i]
                entry_date = df.index[i]

            elif signal == "SELL" and in_trade:
                exit_price = df["Close"].iloc[i]
                exit_date = df.index[i]

                ret = (exit_price - entry_price) / entry_price
                holding_days = (exit_date - entry_date).days

                trades.append({
                    "Return": ret,
                    "Holding_Days": holding_days
                })

                in_trade = False

        trades_df = pd.DataFrame(trades)

        # -------------------------------
        # FILTER LOW DATA
        # -------------------------------
        if trades_df.empty or len(trades_df) < 5:
            continue

        # -------------------------------
        # METRICS
        # -------------------------------
        total_return = trades_df["Return"].sum()
        num_trades = len(trades_df)
        accuracy = (trades_df["Return"] > 0).mean() * 100

        total_days = trades_df["Holding_Days"].sum()
        avg_holding = trades_df["Holding_Days"].mean()

        if total_days > 0:
            annual_return = (1 + total_return) ** (365 / total_days) - 1
        else:
            annual_return = 0

        # -------------------------------
        # CLASSIFICATION
        # -------------------------------
        if annual_return > 0.15 and accuracy > 45:
            category = "Follows SuperTrend"

        elif annual_return < 0:
            category = "Does NOT Follow"

        else:
            category = "Moderate"

        # -------------------------------
        # STORE RESULT
        # -------------------------------
        all_summary.append({
            "Symbol": symbol,
            "Trades": num_trades,
            "Accuracy": accuracy,
            "Annual_Return": annual_return,
            "Avg_Holding_Days": avg_holding,
            "Category": category
        })

    except Exception as e:
        print(f"Error in {symbol}: {e}")
        continue

# -------------------------------
# FINAL OUTPUT
# -------------------------------
final_summary = pd.DataFrame(all_summary)

final_summary.to_csv("../data/securities/final_summary_10_2.csv", index=False)

print("\n✅ FINAL CLEAN FILE CREATED")