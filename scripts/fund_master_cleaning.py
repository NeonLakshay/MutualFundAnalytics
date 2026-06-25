import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/01_fund_master.csv")

print("Original Rows:", len(df))

# Convert launch date
df["launch_date"] = pd.to_datetime(df["launch_date"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Validate AMFI codes
duplicate_amfi = df["amfi_code"].duplicated().sum()

# Validate expense ratio
invalid_expense = (
    (df["expense_ratio_pct"] <= 0)
).sum()

# Save cleaned dataset
df.to_csv(
    "data/processed/01_fund_master_cleaned.csv",
    index=False
)

print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Duplicate AMFI Codes :", duplicate_amfi)
print("Invalid Expense Ratios :", invalid_expense)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/01_fund_master_cleaned.csv")