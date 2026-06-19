import os
import glob
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ---- CONFIG ----
FOLDER = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\data\\bse_bulk_deals"
TABLE  = "stock_market_analysis.bse_bulk_deals"
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

conn = psycopg2.connect(
    host=PG_HOST, port=PG_PORT,
    dbname=PG_DB, user=PG_USER, password=PG_PASS
)

files = sorted(glob.glob(os.path.join(FOLDER, "*.csv")))
print(f"Total files: {len(files)}")

total = 0
for f in files:
    df = pd.read_csv(f, on_bad_lines='skip', encoding='latin1')
    df.columns = [c.strip() for c in df.columns]
    rows = []
    for _, row in df.iterrows():
        rows.append((
            clean_date(row["Deal Date"]),
            str(row["Security Code"]).strip(),
            str(row["Company"]).strip(),
            str(row["Client Name"]).strip(),
            str(row["Deal Type"]).strip(),
            clean_numeric(row["Quantity"]),
            clean_numeric(row["Price"])
        ))
    with conn.cursor() as cur:
        execute_values(cur, f"""
            INSERT INTO {TABLE}
            (deal_date, security_code, company, client_name, deal_type, quantity, price)
            VALUES %s
        """, rows)
    conn.commit()
    total += len(rows)
    print(f"Loaded {os.path.basename(f)}: {len(rows)} rows")

conn.close()
print(f"\nBSE Bulk Deals total loaded: {total} rows!")