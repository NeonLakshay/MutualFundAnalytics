import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "db" / "bluestock_mf.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
]

for table in tables:
    print("\n" + "=" * 60)
    print(table)
    print("=" * 60)

    cursor.execute(f"PRAGMA table_info({table})")

    for col in cursor.fetchall():
        print(col)

conn.close()