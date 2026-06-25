import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/03_aum_by_fund_house.csv")

print("Original Rows:", len(df))

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Validate AUM values
invalid_aum = (df["aum_crore"] <= 0).sum()
df = df[df["aum_crore"] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/03_aum_by_fund_house_cleaned.csv",
    index=False
)

print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid AUM Rows Removed :", invalid_aum)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/03_aum_by_fund_house_cleaned.csv")