import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/06_industry_folio_count.csv")

print("Original Rows:", len(df))

# Convert month column to datetime
df["month"] = pd.to_datetime(df["month"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# List of folio columns
folio_columns = [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]

# Validate all folio values
invalid_rows = 0

for col in folio_columns:
    invalid_rows += (df[col] <= 0).sum()
    df = df[df[col] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/06_industry_folio_count_cleaned.csv",
    index=False
)

# Summary
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid Rows Removed :", invalid_rows)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/06_industry_folio_count_cleaned.csv")