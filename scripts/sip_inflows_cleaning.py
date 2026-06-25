import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")

print("Original Rows:", len(df))

# Convert month to datetime
df["month"] = pd.to_datetime(df["month"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Validate SIP inflow values
invalid_sip = (df["sip_inflow_crore"] <= 0).sum()
df = df[df["sip_inflow_crore"] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/04_monthly_sip_inflows_cleaned.csv",
    index=False
)

# Summary
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid SIP Rows Removed :", invalid_sip)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/04_monthly_sip_inflows_cleaned.csv")