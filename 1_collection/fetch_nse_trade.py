import os
from datetime import date
import psycopg2
import yfinance as yf

PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "postgres"
PG_PASS = "postgres"
TABLE_FQN  = "stock_market_analysis.sec_master"
SYMBOL_COL = "nse_symbol"
START_DATE = "2001-01-01"
END_DATE   = date.today().isoformat()
OUT_DIR    = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\nse_history_csv"

os.makedirs(OUT_DIR, exist_ok=True)

def get_symbols():
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        dbname=PG_DB, user=PG_USER, password=PG_PASS
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT DISTINCT {SYMBOL_COL} "
                f"FROM {TABLE_FQN} "
                f"WHERE {SYMBOL_COL} IS NOT NULL AND {SYMBOL_COL} <> ''"
            )
            return [r[0].strip() for r in cur.fetchall()]
    finally:
        conn.close()

def download_and_save(symbol):
    tkr = f"{symbol}.NS"
    df = yf.download(tkr, start=START_DATE, end=END_DATE, interval="1d", progress=False)
    if df.empty:
        print(f"{symbol}: no data")
        return
    df = df.reset_index()
    df.insert(0, "Symbol", symbol)
    out_path = os.path.join(OUT_DIR, f"{symbol}.csv")
    df.to_csv(out_path, index=False)
    print(f"{symbol}: {len(df)} rows saved")

def main():
    symbols = get_symbols()
    if not symbols:
        print("No symbols found.")
        return
    print(f"Found {len(symbols)} NSE symbols. Starting download...")
    for s in symbols:
        try:
            download_and_save(s)
        except Exception as e:
            print(f"{s}: ERROR -> {e}")

if __name__ == "__main__":
    main()