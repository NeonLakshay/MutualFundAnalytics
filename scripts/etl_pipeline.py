import pandas as pd
from sqlalchemy import create_engine, text

# ------------------------------------------
# Connect to SQLite Database
# ------------------------------------------

engine = create_engine("sqlite:///bluestock_mf.db")

print("Connected to SQLite Database Successfully!")

with engine.begin() as conn:
    conn.execute(text("DELETE FROM fact_nav"))
    conn.execute(text("DELETE FROM fact_transactions"))
    conn.execute(text("DELETE FROM fact_performance"))
    conn.execute(text("DELETE FROM dim_date"))
    conn.execute(text("DELETE FROM dim_fund"))

print("Existing data cleared successfully!")

# ---------------------------------------
# Load Dimension Table : dim_fund
# ---------------------------------------

print("\nLoading dim_fund...")

fund_df = pd.read_csv("data/raw/01_fund_master.csv")

# print(fund_df.columns.tolist())


# Keep only required columns
dim_fund = fund_df[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "plan",
        "risk_category",
    ]
].copy()

# Rename column to match database schema
dim_fund.rename(
    columns={"risk_category": "risk_grade"},
    inplace=True
)

# Remove duplicate records
dim_fund = dim_fund.drop_duplicates()

# Load into SQLite
dim_fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)

print(f"dim_fund loaded successfully! ({len(dim_fund)} rows)")

# ---------------------------------------
# Load Dimension Table : dim_date
# ---------------------------------------

print("\nLoading dim_date...")

# Read cleaned datasets
nav_df = pd.read_csv("data/processed/02_nav_history_cleaned.csv")
transaction_df = pd.read_csv("data/processed/08_investor_transactions_cleaned.csv")

# Convert to datetime
nav_df["date"] = pd.to_datetime(nav_df["date"])
transaction_df["transaction_date"] = pd.to_datetime(
    transaction_df["transaction_date"]
)

# Collect all unique dates
all_dates = pd.concat(
    [
        nav_df["date"],
        transaction_df["transaction_date"]
    ]
).drop_duplicates().sort_values()

# Create Date Dimension
dim_date = pd.DataFrame()

dim_date["date"] = all_dates.values

dim_date["year"] = dim_date["date"].dt.year
dim_date["month"] = dim_date["date"].dt.month
dim_date["day"] = dim_date["date"].dt.day
dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)

# Load into SQLite
dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

print(f"dim_date loaded successfully! ({len(dim_date)} rows)")

# ---------------------------------------
# Load Fact Table : fact_nav
# ---------------------------------------

print("\nLoading fact_nav...")

# Read dim_date from SQLite
date_lookup = pd.read_sql(
    "SELECT date_id, date FROM dim_date",
    engine
)

# Convert date column to datetime
date_lookup["date"] = pd.to_datetime(date_lookup["date"])

# Read cleaned NAV dataset
nav_df = pd.read_csv(
    "data/processed/02_nav_history_cleaned.csv"
)

# Convert date column to datetime
nav_df["date"] = pd.to_datetime(nav_df["date"])

# Map date -> date_id
nav_df = nav_df.merge(
    date_lookup,
    on="date",
    how="left"
)

# Keep only required columns
fact_nav = nav_df[
    [
        "amfi_code",
        "date_id",
        "nav"
    ]
]

# Load into SQLite
fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

print(f"fact_nav loaded successfully! ({len(fact_nav)} rows)")

# ---------------------------------------
# Load Fact Table : fact_transactions
# ---------------------------------------

print("\nLoading fact_transactions...")

# Read cleaned transaction dataset
transaction_df = pd.read_csv(
    "data/processed/08_investor_transactions_cleaned.csv"
)

# Convert transaction date to datetime
transaction_df["transaction_date"] = pd.to_datetime(
    transaction_df["transaction_date"]
)

# Read date lookup table
date_lookup = pd.read_sql(
    "SELECT date_id, date FROM dim_date",
    engine
)

date_lookup["date"] = pd.to_datetime(date_lookup["date"])

# Map transaction_date -> date_id
transaction_df = transaction_df.merge(
    date_lookup,
    left_on="transaction_date",
    right_on="date",
    how="left"
)

# Select required columns
fact_transactions = transaction_df[
    [
        "investor_id",
        "amfi_code",
        "date_id",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
]

# Load into SQLite
fact_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

print(
    f"fact_transactions loaded successfully! ({len(fact_transactions)} rows)"
)

# ---------------------------------------
# Load Fact Table : fact_performance
# ---------------------------------------

print("\nLoading fact_performance...")

performance_df = pd.read_csv(
    "data/processed/07_scheme_performance_cleaned.csv"
)

fact_performance = performance_df[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "expense_ratio_pct",
        "morningstar_rating"
    ]
]

fact_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

print(
    f"fact_performance loaded successfully! ({len(fact_performance)} rows)"
)

# ---------------------------------------
# Load Fact Table : fact_aum
# ---------------------------------------

print("\nLoading fact_aum...")

# Read AUM dataset
aum_df = pd.read_csv(
    "data/raw/03_aum_by_fund_house.csv"
)

# Convert date column
aum_df["date"] = pd.to_datetime(aum_df["date"])

# Read date lookup
date_lookup = pd.read_sql(
    "SELECT date_id, date FROM dim_date",
    engine
)

date_lookup["date"] = pd.to_datetime(date_lookup["date"])

# Map date -> date_id
aum_df = aum_df.merge(
    date_lookup,
    on="date",
    how="left"
)

# Keep required columns
fact_aum = aum_df[
    [
        "fund_house",
        "date_id",
        "aum_crore"
    ]
]

# Load into SQLite
fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

print(
    f"fact_aum loaded successfully! ({len(fact_aum)} rows)"
)

# ---------------------------------------
# Verify Row Counts
# ---------------------------------------

print("\n")
print("=" * 60)
print("ROW COUNT VERIFICATION")
print("=" * 60)

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in tables:

    count = pd.read_sql(
        f"SELECT COUNT(*) AS rows FROM {table}",
        engine
    )

    print(f"{table:<22} : {count.iloc[0,0]} rows")

print("=" * 60)
print("ETL Pipeline Completed Successfully!")