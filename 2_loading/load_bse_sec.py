import csv
import psycopg2

csv_file = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\data\\1-bse_securities_31012026.csv"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

insert_sql = """
INSERT INTO stock_market_analysis.bse_securities
(sec_code, issuer_name, symbol, company_name, status, "group", face_val, isin_num, instrument)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

def clean_numeric(val):
    val = val.strip()
    if val == "-" or val == "":
        return None
    try:
        return float(val)
    except:
        return None

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v for k, v in row.items()}
        cur.execute(insert_sql, (
            row["Security Code"],
            row["Issuer Name"],
            row["Security Id"],
            row["Security Name"],
            row["Status"],
            row["Group"],
            clean_numeric(row["Face Value"]),
            row["ISIN No"],
            row["Instrument"]
        ))

conn.commit()
cur.close()
conn.close()
print("BSE Securities inserted successfully!")