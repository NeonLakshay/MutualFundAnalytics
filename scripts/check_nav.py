import sqlite3
import pandas as pd

conn = sqlite3.connect("db/bluestock_mf.db")

print("=" * 60)
print("DIM_FUND")
print("=" * 60)

print(pd.read_sql("""
SELECT amfi_code, scheme_name
FROM dim_fund
LIMIT 10
""", conn))

print()

print("=" * 60)
print("FACT_NAV")
print("=" * 60)

print(pd.read_sql("""
SELECT amfi_code, COUNT(*) AS total
FROM fact_nav
GROUP BY amfi_code
LIMIT 10
""", conn))

conn.close()