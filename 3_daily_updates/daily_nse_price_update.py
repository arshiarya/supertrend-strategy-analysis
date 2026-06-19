import psycopg2
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from psycopg2.extras import execute_values

# ---- CONFIG ----
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "postgres"
PG_PASS = "postgres"
TABLE  = "stock_market_analysis.nse_trade_daily"
MASTER = "stock_market_analysis.sec_master"
# ----------------

def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        dbname=PG_DB, user=PG_USER, password=PG_PASS
    )

def get_symbols(conn):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT DISTINCT nse_symbol FROM {MASTER} "
            f"WHERE nse_symbol IS NOT NULL AND nse_symbol <> ''"
        )
        return [str(row[0]).strip() for row in cur.fetchall()]

def get_last_date(conn, symbol):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT MAX(trade_date) FROM {TABLE} WHERE symbol = %s",
            (symbol,)
        )
        row = cur.fetchone()
        if row is None or row[0] is None:
            return date(2001, 1, 1)
        return row[0]

def download_new_data(symbol, last_date):
    start = (last_date + timedelta(days=1)).isoformat()
    end   = date.today().isoformat()

    if start >= end:
        return None

    df = yf.download(
        f"{symbol}.NS",
        start=start, end=end,
        interval="1d", progress=False
    )
    if df.empty:
        return None

    # Fix yFinance MultiIndex columns like ('Close', 'HALDER') → 'close'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0].strip().lower() for col in df.columns]
    else:
        df.columns = [c.strip().lower() for c in df.columns]

    df = df.reset_index()
    df.insert(0, "Symbol", symbol)

    # Rename columns
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={
        "date":     "trade_date",
        "datetime": "trade_date",
        "close":    "close_price",
        "high":     "high_price",
        "low":      "low_price",
        "open":     "open_price"
    })

    cols = ["symbol", "trade_date", "close_price", "high_price", "low_price", "open_price", "volume"]

    # Check all columns exist
    missing = [c for c in cols if c not in df.columns]
    if missing:
        print(f"{symbol}: missing columns {missing}")
        return None

    df = df[cols]
    df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce").dt.date
    for c in ["close_price", "high_price", "low_price", "open_price", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["symbol", "trade_date"])

    return df

def insert_data(conn, df):
    rows = list(df.itertuples(index=False, name=None))
    with conn.cursor() as cur:
        execute_values(cur, f"""
            INSERT INTO {TABLE}
            (symbol, trade_date, close_price, high_price, low_price, open_price, volume)
            VALUES %s
            ON CONFLICT (symbol, trade_date) DO NOTHING
        """, rows)
    conn.commit()
    return len(rows)

def main():
    conn = get_conn()
    symbols = get_symbols(conn)
    print(f"Total NSE symbols : {len(symbols)}")
    print(f"Checking for new data...\n")

    total_new  = 0
    up_to_date = 0

    for s in symbols:
        try:
            last_date = get_last_date(conn, s)
            df = download_new_data(s, last_date)

            if df is None:
                up_to_date += 1
                continue

            n = insert_data(conn, df)
            total_new += n
            print(f"{s}: {n} new rows added (was up to {last_date})")

        except Exception as e:
            print(f"{s}: ERROR -> {e}")

    conn.close()
    print(f"\nDone!")
    print(f"Stocks already up to date : {up_to_date}")
    print(f"Total new rows inserted   : {total_new}")

if __name__ == "__main__":
    main()