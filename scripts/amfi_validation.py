import pandas as pd

# Load datasets
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

# Unique AMFI codes
master_codes = set(fund_master["amfi_code"].unique())
nav_codes = set(nav_history["amfi_code"].unique())

# Missing codes
missing_codes = master_codes - nav_codes

print("\nAMFI CODE VALIDATION")
print("=" * 50)

print(f"AMFI Codes in fund_master : {len(master_codes)}")
print(f"AMFI Codes in nav_history : {len(nav_codes)}")

print(f"\nMissing Codes : {len(missing_codes)}")

if len(missing_codes) > 0:
    print("\nMissing AMFI Codes:")
    print(sorted(missing_codes))
else:
    print("\nAll AMFI codes from fund_master exist in nav_history.")

print("\nDATA QUALITY SUMMARY")
print("=" * 50)

if len(missing_codes) == 0:
    print("""
1. All AMFI codes from fund_master are present in nav_history.
2. No missing schemes found.
3. Dataset passes completeness validation.
4. Data quality is good.
""")
else:
    print(f"""
1. Missing AMFI Codes: {len(missing_codes)}
2. Some schemes are missing from nav_history.
3. Dataset fails completeness validation.
4. Further investigation required.
""")