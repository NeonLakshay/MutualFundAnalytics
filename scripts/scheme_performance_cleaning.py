import pandas as pd

# ============================================
# Load Dataset
# ============================================

df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Original Rows:", len(df))


# ============================================
# Validate Return Columns are Numeric
# ============================================

return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

invalid_return_values = 0

for column in return_columns:

    # Convert to numeric (invalid values become NaN)
    df[column] = pd.to_numeric(df[column], errors="coerce")

    # Count invalid values
    invalid_return_values += df[column].isnull().sum()

# Remove rows having invalid return values
df = df.dropna(subset=return_columns)


# ============================================
# Flag Return Anomalies
# (Outside realistic range)
# ============================================

return_anomalies = (
    (df[return_columns] < -100) |
    (df[return_columns] > 200)
).sum().sum()


# ============================================
# Validate Expense Ratio
# Valid Range : 0.1% to 2.5%
# ============================================

expense_ratio_violations = (
    (df["expense_ratio_pct"] < 0.1) |
    (df["expense_ratio_pct"] > 2.5)
).sum()


# ============================================
# Save Cleaned Dataset
# ============================================

df.to_csv(
    "data/processed/07_scheme_performance_cleaned.csv",
    index=False
)


# ============================================
# Cleaning Summary
# ============================================

print("\nCleaning Completed Successfully!")
print("------------------------------------------")

print("Invalid Return Values Found :", invalid_return_values)

print("Return Anomalies Found      :", return_anomalies)

print("Expense Ratio Violations    :", expense_ratio_violations)

print("Final Rows                  :", len(df))

print("\nCleaned file saved to:")

print("data/processed/07_scheme_performance_cleaned.csv")