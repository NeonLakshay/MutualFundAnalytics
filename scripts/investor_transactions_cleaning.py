import pandas as pd

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
df = pd.read_csv("data/raw/08_investor_transactions.csv")

print("Original Rows:", len(df))

# -------------------------------------------------
# 1. Fix transaction_date format
# -------------------------------------------------
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

invalid_dates = df["transaction_date"].isna().sum()

# Remove rows having invalid dates
df = df.dropna(subset=["transaction_date"])

# -------------------------------------------------
# 2. Remove duplicate rows
# -------------------------------------------------
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# -------------------------------------------------
# 3. Validate transaction amount (> 0)
# -------------------------------------------------
invalid_amounts = (df["amount_inr"] <= 0).sum()

# Remove invalid amount rows
df = df[df["amount_inr"] > 0]

print("\nAmount Validation")
print("-----------------")
print("Invalid Amount Rows :", invalid_amounts)

if invalid_amounts == 0:
    print("All transaction amounts are valid.")
else:
    print("Invalid amount rows removed.")

# -------------------------------------------------
# 4. Validate transaction types
# -------------------------------------------------
expected_transaction_types = {
    "SIP",
    "Lumpsum",
    "Redemption"
}

actual_transaction_types = set(df["transaction_type"].unique())

print("\nTransaction Type Validation")
print("---------------------------")
print("Expected :", expected_transaction_types)
print("Found    :", actual_transaction_types)

if actual_transaction_types == expected_transaction_types:
    print("Transaction types are valid.")
else:
    print("Unexpected transaction types found!")

# -------------------------------------------------
# 5. Validate KYC status values
# -------------------------------------------------
expected_kyc = {
    "Verified",
    "Pending"
}

actual_kyc = set(df["kyc_status"].unique())

print("\nKYC Status Validation")
print("---------------------")
print("Expected :", expected_kyc)
print("Found    :", actual_kyc)

if actual_kyc == expected_kyc:
    print("KYC status values are valid.")
else:
    print("Unexpected KYC status values found!")

# -------------------------------------------------
# Save cleaned dataset
# -------------------------------------------------
df.to_csv(
    "data/processed/08_investor_transactions_cleaned.csv",
    index=False
)

# -------------------------------------------------
# Cleaning Summary
# -------------------------------------------------
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Date Format Fixed : transaction_date converted to datetime")
print("Invalid Date Rows Removed :", invalid_dates)
print("Duplicate Rows Removed :", duplicates)
print("Invalid Amount Rows Removed :", invalid_amounts)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/08_investor_transactions_cleaned.csv")