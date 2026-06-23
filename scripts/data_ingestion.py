import pandas as pd

# Load fund master dataset
fund_master = pd.read_csv("data/raw/01_fund_master.csv")

print("\nUnique Fund Houses:")
print(fund_master["fund_house"].unique())

print("\nCategories:")
print(fund_master["category"].unique())

print("\nSub-Categories:")
print(fund_master["sub_category"].unique())

print("\nRisk Grades:")
print(fund_master["risk_category"].unique())