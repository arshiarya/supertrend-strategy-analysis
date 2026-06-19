import csv
import psycopg2

csv_file = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\data\\2-nse_securities_31012026.csv"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

insert_sql = """
INSERT INTO stock_market_analysis.nse_securities
(symbol, company_name, series, dt_of_listing, paid_up_val, market_lot, isin_num, face_val)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v for k, v in row.items()}
        cur.execute(insert_sql, (
            row["SYMBOL"],
            row["NAME OF COMPANY"],
            row["SERIES"],
            row["DATE OF LISTING"],
            row["PAID UP VALUE"],
            row["MARKET LOT"],
            row["ISIN NUMBER"],
            row["FACE VALUE"]
        ))

conn.commit()
cur.close()
conn.close()
print("NSE Securities inserted successfully!")