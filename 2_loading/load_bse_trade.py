import os, glob
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ---- CONFIG ----
FOLDER = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\bse_history_csv"
TABLE  = "stock_market_analysis.bse_trade_daily"
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "postgres"
PG_PASS = "postgres"
MAX_WORKERS = 8
# ----------------

COLS = ["symbol", "trade_date", "close_price", "high_price", "low_price", "open_price", "volume"]

def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS
    )

def load_one(csv_path: str):
    try:
        df = pd.read_csv(csv_path, skiprows=[1])
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.rename(columns={
            "date":  "trade_date",
            "close": "close_price",
            "high":  "high_price",
            "low":   "low_price",
            "open":  "open_price"
        })
        df = df[COLS]
        df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce").dt.date
        for c in ["close_price", "high_price", "low_price", "open_price", "volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df.dropna(subset=["symbol", "trade_date"])
        if df.empty:
            return (os.path.basename(csv_path), 0, "OK (no rows)")
        rows = list(df.itertuples(index=False, name=None))
        with get_conn() as conn, conn.cursor() as cur:
            execute_values(cur, f"""
                INSERT INTO {TABLE} ({", ".join(COLS)}) VALUES %s
                ON CONFLICT (symbol, trade_date) DO NOTHING;
            """, rows, page_size=len(rows))
            conn.commit()
        return (os.path.basename(csv_path), len(rows), "OK")
    except Exception as e:
        return (os.path.basename(csv_path), 0, f"ERROR: {e}")

def main():
    files = sorted(glob.glob(os.path.join(FOLDER, "*.csv")))
    if not files:
        print(f"No CSVs found in: {FOLDER}")
        return
    print(f"Found {len(files)} files. Uploading with {MAX_WORKERS} threads...\n")
    ok, err, total = 0, 0, 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = [pool.submit(load_one, f) for f in files]
        for fut in as_completed(futs):
            fname, n, status = fut.result()
            if status.startswith("OK"):
                ok += 1
                total += n
                print(f"[OK]   {fname}: {n} rows")
            else:
                err += 1
                print(f"[FAIL] {fname}: {status}")
    print(f"\nDone. Files OK: {ok} | Files failed: {err} | Rows inserted: {total:,}")

if __name__ == "__main__":
    main()