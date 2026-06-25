import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/02_nav_history.csv")

print("Original Rows:", len(df))

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by AMFI code and date
df = df.sort_values(by=["amfi_code", "date"])

# Forward-fill missing NAV values within each scheme
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Remove invalid NAV values (<= 0)
invalid_nav = (df["nav"] <= 0).sum()
df = df[df["nav"] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/02_nav_history_cleaned.csv",
    index=False
)

# Summary
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid NAV Rows Removed :", invalid_nav)
print("Final Rows :", len(df))
print("\nCleaned file saved to:")
print("data/processed/02_nav_history_cleaned.csv")