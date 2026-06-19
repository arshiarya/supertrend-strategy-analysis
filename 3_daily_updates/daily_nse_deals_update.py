import psycopg2
import pandas as pd
from datetime import date
from nselib import capital_market
from psycopg2.extras import execute_values

# ---- CONFIG ----
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "postgres"
PG_PASS = "postgres"
BULK_TABLE  = "stock_market_analysis.nse_bulk_deals"
BLOCK_TABLE = "stock_market_analysis.nse_block_deals"
# ----------------

def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        dbname=PG_DB, user=PG_USER, password=PG_PASS
    )

def get_last_date(conn, table):
    with conn.cursor() as cur:
        cur.execute(f"SELECT MAX(trade_date) FROM {table}")
        row = cur.fetchone()
        if row is None or row[0] is None:
            return "01-01-2001"
        return row[0].strftime("%d-%m-%Y")

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

def update_bulk_deals(conn):
    last_date = get_last_date(conn, BULK_TABLE)
    to_dt     = date.today().strftime("%d-%m-%Y")
    print(f"Fetching NSE bulk deals from {last_date} to {to_dt}...")
    data = capital_market.bulk_deal_data(from_date=last_date, to_date=to_dt)
    df   = pd.DataFrame(data)
    if df.empty:
        print("NSE Bulk Deals: no new data!")
        return 0
    df.columns = [c.strip() for c in df.columns]
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
    with conn.cursor() as cur:
        execute_values(cur, f"""
            INSERT INTO {BULK_TABLE}
            (trade_date, symbol, security_name, client_name, buy_sell, quantity, trade_price, remarks)
            VALUES %s
            ON CONFLICT (trade_date, symbol, client_name, buy_sell) DO NOTHING
        """, rows)
    conn.commit()
    print(f"NSE Bulk Deals: {len(rows)} rows processed!")
    return len(rows)

def update_block_deals(conn):
    last_date = get_last_date(conn, BLOCK_TABLE)
    to_dt     = date.today().strftime("%d-%m-%Y")
    print(f"Fetching NSE block deals from {last_date} to {to_dt}...")
    data = capital_market.block_deals_data(from_date=last_date, to_date=to_dt)
    df   = pd.DataFrame(data)
    if df.empty:
        print("NSE Block Deals: no new data!")
        return 0
    df.columns = [c.strip() for c in df.columns]
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
    with conn.cursor() as cur:
        execute_values(cur, f"""
            INSERT INTO {BLOCK_TABLE}
            (trade_date, symbol, security_name, client_name, buy_sell, quantity, trade_price, remarks)
            VALUES %s
            ON CONFLICT (trade_date, symbol, client_name, buy_sell) DO NOTHING
        """, rows)
    conn.commit()
    print(f"NSE Block Deals: {len(rows)} rows processed!")
    return len(rows)

def main():
    conn = get_conn()
    print("=== NSE Daily Deals Update ===\n")
    bulk_rows  = update_bulk_deals(conn)
    print()
    block_rows = update_block_deals(conn)
    conn.close()
    print(f"\nDone!")
    print(f"NSE Bulk Deals processed  : {bulk_rows}")
    print(f"NSE Block Deals processed : {block_rows}")

if __name__ == "__main__":
    main()

