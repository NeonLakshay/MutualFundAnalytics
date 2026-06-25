import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/09_portfolio_holdings.csv")

print("Original Rows:", len(df))

# Convert portfolio date
df["portfolio_date"] = pd.to_datetime(df["portfolio_date"])

# Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Validate weight percentage
invalid_weight = (
    (df["weight_pct"] < 0) |
    (df["weight_pct"] > 100)
).sum()

df = df[
    (df["weight_pct"] >= 0) &
    (df["weight_pct"] <= 100)
]

# Validate market value
invalid_market_value = (df["market_value_cr"] <= 0).sum()
df = df[df["market_value_cr"] > 0]

# Validate stock price
invalid_price = (df["current_price_inr"] <= 0).sum()
df = df[df["current_price_inr"] > 0]

# Save cleaned dataset
df.to_csv(
    "data/processed/09_portfolio_holdings_cleaned.csv",
    index=False
)

# Summary
print("\nCleaning Completed Successfully!")
print("--------------------------------")
print("Duplicate Rows Removed :", duplicates)
print("Invalid Weight Rows Removed :", invalid_weight)
print("Invalid Market Value Rows Removed :", invalid_market_value)
print("Invalid Price Rows Removed :", invalid_price)
print("Final Rows :", len(df))

print("\nCleaned file saved to:")
print("data/processed/09_portfolio_holdings_cleaned.csv")