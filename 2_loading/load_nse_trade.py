import os
import pandas as pd
import psycopg2

FOLDER = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\nse_history_csv"
TABLE  = "stock_market_analysis.nse_trade_daily"

conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="postgres", user="postgres", password="postgres"
)

files = [f for f in os.listdir(FOLDER) if f.endswith(".csv")]
print(f"Total files: {len(files)}")

for f in files:
    df = pd.read_csv(os.path.join(FOLDER, f), skiprows=[1])
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={
        "date":  "trade_date",
        "close": "close_price",
        "high":  "high_price",
        "low":   "low_price",
        "open":  "open_price"
    })
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(f"""
                INSERT INTO {TABLE}
                (symbol, trade_date, close_price, high_price, low_price, open_price, volume)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (symbol, trade_date) DO NOTHING
            """, (
                row["symbol"], row["trade_date"], row["close_price"],
                row["high_price"], row["low_price"], row["open_price"], row["volume"]
            ))
    conn.commit()
    print(f"Uploaded: {f}")

conn.close()
print("NSE trade history upload complete!")