import sqlite3

# Create/connect to SQLite database
conn = sqlite3.connect("bluestock_mf.db")

# Read schema.sql
with open("sql/schema.sql", "r") as f:
    schema = f.read()

# Execute SQL
conn.executescript(schema)

conn.commit()
conn.close()

print("Database and tables created successfully!")