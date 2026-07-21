import sqlite3
import pandas as pd

conn = sqlite3.connect("db/bluestock_mf.db")

print("\n===== First 5 rows of fact_nav =====")

df = pd.read_sql("""
SELECT *
FROM fact_nav
LIMIT 5
""", conn)

print(df)

print("\n===== Distinct AMFI Codes =====")

codes = pd.read_sql("""
SELECT DISTINCT amfi_code
FROM fact_nav
ORDER BY amfi_code
""", conn)

print(codes)

conn.close()