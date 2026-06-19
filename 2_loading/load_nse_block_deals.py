import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ---- CONFIG ----
FILE  = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\data\\nse_block_deals\\blockdeals_23-03-2026.csv"
TABLE = "stock_market_analysis.nse_block_deals"
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "postgres"
PG_PASS = "postgres"
# ----------------

def clean_numeric(val):
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return None

def clean_date(val):
    try:
        return pd.to_datetime(val, dayfirst=True).date()
    except:
        return None

df = pd.read_csv(FILE)
df.columns = [c.strip() for c in df.columns]

print(f"Total rows: {len(df)}")

rows = []
for _, row in df.iterrows():
    rows.append((
        clean_date(row["Date"]),
        str(row["Symbol"]).strip(),
        str(row["SecurityName"]).strip(),
        str(row["ClientName"]).strip(),
        str(row["Buy/Sell"]).strip(),
        clean_numeric(row["QuantityTraded"]),
        clean_numeric(row["TradePrice/Wght.Avg.Price"]),
        str(row["Remarks"]).strip()
    ))

conn = psycopg2.connect(
    host=PG_HOST, port=PG_PORT,
    dbname=PG_DB, user=PG_USER, password=PG_PASS
)
with conn.cursor() as cur:
    execute_values(cur, f"""
        INSERT INTO {TABLE}
        (trade_date, symbol, security_name, client_name, buy_sell, quantity, trade_price, remarks)
        VALUES %s
    """, rows)
conn.commit()
conn.close()
print(f"NSE Block Deals loaded: {len(rows)} rows!")