import pandas as pd

# Load raw dataset
df = pd.read_csv("./data/raw/05_category_inflows.csv")

print("Original Rows:", len(df))

# -----------------------------
# Clean column names
# -----------------------------
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("-", "_")
)

# -----------------------------
# Convert month to datetime
# -----------------------------
df["month"] = pd.to_datetime(df["month"])

# -----------------------------
# Clean numeric column ONLY
# -----------------------------
df["net_inflow_crore"] = (
    df["net_inflow_crore"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .astype(float)
)

# -----------------------------
# Remove duplicates
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Fill missing values
# -----------------------------
df["category"] = df["category"].fillna("Unknown")
df["net_inflow_crore"] = df["net_inflow_crore"].fillna(0)

# -----------------------------
# Save cleaned file
# -----------------------------
output_path = "./data/processed/05_category_inflows_cleaned.csv"

df.to_csv(output_path, index=False)

print("Cleaned Rows:", len(df))
print("Saved Successfully!")
print(df.head())