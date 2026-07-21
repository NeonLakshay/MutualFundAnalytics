from pathlib import Path
import sqlite3

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

DB_PATH = BASE_DIR / "db" / "bluestock_mf.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

# ----------------------------------------------------
# Create / Connect SQLite Database
# ----------------------------------------------------
conn = sqlite3.connect(DB_PATH)

# Enable Foreign Key Constraints
conn.execute("PRAGMA foreign_keys = ON;")

# ----------------------------------------------------
# Read SQL Schema
# ----------------------------------------------------
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = f.read()

# ----------------------------------------------------
# Create Tables
# ----------------------------------------------------
conn.executescript(schema)

conn.commit()
conn.close()

print("Database and tables created successfully!")