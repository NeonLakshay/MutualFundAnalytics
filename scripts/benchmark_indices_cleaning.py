import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/10_benchmark_indices.csv")

print("Original Rows:", len(df))

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Validate close value
invalid_close = (df["close_value"] <= 0).sum()
df = df[df["close_value"] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/10_benchmark_indices_cleaned.csv",
    index=False
)

# Summary
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid Close Value Rows Removed :", invalid_close)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/10_benchmark_indices_cleaned.csv")