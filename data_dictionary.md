# BlueStock Mutual Fund Analytics

# Data Dictionary

---

## Project Information

| Item | Details |
|------|---------|
| Project Name | BlueStock Mutual Fund Analytics |
| Domain | Financial Data Engineering |
| Database | SQLite |
| Language | Python |
| Data Processing | Pandas |
| SQL Engine | SQLAlchemy + SQLite |
| Prepared By | Lakshay |
| Version | 1.0 |

---

# Project Overview

The BlueStock Mutual Fund Analytics project is an end-to-end Data Engineering pipeline developed to ingest, clean, validate, transform, store, and analyze Indian Mutual Fund datasets.

The project follows a complete ETL (Extract, Transform, Load) workflow.

The final output consists of:

- Cleaned datasets
- SQLite Data Warehouse
- Star Schema
- Analytical SQL Queries
- Data Dictionary
- Documentation

---

# Source Datasets

| Dataset | Description |
|----------|-------------|
| 01_fund_master.csv | Master information for all mutual fund schemes |
| 02_nav_history.csv | Historical Net Asset Value (NAV) records |
| 03_aum_by_fund_house.csv | Assets Under Management for fund houses |
| 04_monthly_sip_inflows.csv | Monthly SIP investments |
| 05_category_inflows.csv | Category-wise investment inflows |
| 06_industry_folio_count.csv | Industry folio statistics |
| 07_scheme_performance.csv | Mutual fund performance metrics |
| 08_investor_transactions.csv | Individual investor transaction records |
| 09_portfolio_holdings.csv | Portfolio allocation of mutual funds |
| 10_benchmark_indices.csv | Benchmark market index data |

---

# Dataset 1 : Fund Master

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 01_fund_master.csv |
| Purpose | Stores the master information for every mutual fund scheme available in the project. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | amfi_code |
| Total Records | 40 |
| Used In | dim_fund |
| Cleaning Required | No major cleaning required |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| amfi_code | Integer | Unique AMFI code identifying each mutual fund scheme. |
| fund_house | Text | Name of the Asset Management Company (AMC). |
| scheme_name | Text | Official name of the mutual fund scheme. |
| category | Text | Fund category (Equity, Debt, Hybrid, etc.). |
| sub_category | Text | More specific classification within the category. |
| plan | Text | Scheme plan (Regular or Direct). |
| launch_date | Date | Date on which the mutual fund scheme was launched. |
| benchmark | Text | Benchmark index used to compare fund performance. |
| expense_ratio_pct | Float | Annual expense ratio charged by the AMC. |
| exit_load_pct | Float | Exit load charged when redeeming units before the specified holding period. |
| min_sip_amount | Float | Minimum amount required to start a SIP. |
| min_lumpsum_amount | Float | Minimum one-time investment amount. |
| fund_manager | Text | Name of the fund manager responsible for managing the scheme. |
| risk_category | Text | Risk classification assigned to the scheme (Low, Moderate, High, Very High). |
| sebi_category_code | Text | Official SEBI category code for the mutual fund scheme. |

---

## Business Rules

- Each mutual fund scheme must have a unique **AMFI Code**.
- One fund house can manage multiple mutual fund schemes.
- Expense ratio is expressed as a percentage.
- SIP and Lumpsum minimum investment amounts must always be positive.
- Every scheme belongs to exactly one category and one sub-category.

---

## Cleaning Rules Applied

- Verified all AMFI Codes are unique.
- Verified no missing values in primary key.
- Preserved original fund metadata.
- Used as the source table for the **dim_fund** dimension in the SQLite Star Schema.

---

# Dataset 2 : NAV History

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 02_nav_history.csv |
| Purpose | Stores the historical daily Net Asset Value (NAV) of every mutual fund scheme. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | (amfi_code + date) |
| Total Records | 46,000 |
| Used In | fact_nav |
| Cleaning Required | Yes |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| amfi_code | Integer | Unique AMFI code identifying the mutual fund scheme. |
| date | Date | Date on which the NAV was recorded. |
| nav | Float | Net Asset Value (NAV) of one unit of the mutual fund on the given date. |

---

## Business Rules

- One NAV value exists for each mutual fund scheme on each trading day.
- NAV values must always be greater than zero.
- Each (amfi_code, date) combination should be unique.
- NAV is not published on weekends and market holidays.
- Missing NAV values due to non-trading days are forward-filled using the previous available trading day's NAV.

---

## Cleaning Rules Applied

- Converted the **date** column to DateTime format.
- Sorted the dataset by **amfi_code** and **date**.
- Forward-filled missing NAV values within each mutual fund scheme.
- Removed duplicate records.
- Removed invalid NAV values (NAV ≤ 0).
- Saved the cleaned dataset as:

```text
data/processed/02_nav_history_cleaned.csv
```

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| fact_nav | Stores historical NAV values |
| dim_fund | Connected using amfi_code |
| dim_date | Connected using date_id |

---

# Dataset 3 : AUM by Fund House

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 03_aum_by_fund_house.csv |
| Purpose | Stores Assets Under Management (AUM) of different fund houses over time. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | (fund_house + date) |
| Used In | fact_aum |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| fund_house | Text | Name of the Asset Management Company (AMC). |
| date | Date | Reporting date for the AUM value. |
| aum_crore | Float | Total Assets Under Management (AUM) in Crores (INR). |

---

## Business Rules

- AUM represents the total market value of assets managed by a fund house.
- AUM values must always be positive.
- One AUM value exists for each fund house on each reporting date.
- Higher AUM generally indicates a larger fund house.

---

## Cleaning Rules Applied

- Converted **date** column to DateTime format.
- Verified AUM values are numeric.
- Validated AUM values are greater than zero.
- Removed duplicate records (if any).
- Loaded into SQLite as **fact_aum**.

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| fact_aum | Stores Assets Under Management |
| dim_date | Connected using date_id |

---

# Dataset 4 : Monthly SIP Inflows

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 04_monthly_sip_inflows.csv |
| Purpose | Stores monthly SIP (Systematic Investment Plan) investment inflows across mutual funds. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | month |
| Used In | Business Analytics |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| month | Date | Reporting month of SIP inflows. |
| sip_inflow_crore | Float | Total SIP investment received during the month (in Crores INR). |

---

## Business Rules

- One record represents one month's total SIP inflow.
- SIP inflow values must always be positive.
- Month values should be unique.
- Data is used for trend analysis and Year-over-Year (YoY) growth analysis.

---

## Cleaning Rules Applied

- Converted **month** column to DateTime format.
- Verified SIP inflow values are numeric.
- Validated SIP inflow values are greater than zero.
- Removed duplicate records (if any).

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| Used for Analytics | Monthly SIP Trend Analysis |
| dim_date | Can be joined using the month/date field |

---

# Dataset 5 : Category Inflows

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 05_category_inflows.csv |
| Purpose | Stores category-wise investment inflows into different mutual fund categories. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | (category + month) |
| Used In | Business Analytics |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| category | Text | Mutual fund category (Equity, Debt, Hybrid, etc.). |
| month | Date | Reporting month of the investment inflow. |
| inflow_crore | Float | Total investment inflow into the category (in Crores INR). |

---

## Business Rules

- Each category has one inflow value for each reporting month.
- Inflow values must be numeric.
- Investment inflows may be positive or negative.
- Positive values indicate net investments.
- Negative values indicate net outflows (more money withdrawn than invested).

---

## Cleaning Rules Applied

- Converted **month** column to DateTime format.
- Verified inflow values are numeric.
- Removed duplicate records (if any).
- Preserved both positive and negative values because outflows are valid business events.

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| Used for Analytics | Category-wise Investment Trend Analysis |
| dim_date | Can be joined using the month/date field |

---

# Dataset 6 : Industry Folio Count

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 06_industry_folio_count.csv |
| Purpose | Stores the total number of investor folios across the mutual fund industry. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | month |
| Used In | Industry Analysis |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| month | Date | Reporting month of the folio count. |
| folio_count | Integer | Total number of investor folios during the reporting month. |

---

## Business Rules

- One record represents one month's folio count.
- Folio count must always be positive.
- Used to analyze investor participation trends.

---

## Cleaning Rules Applied

- Converted month column to DateTime format.
- Verified folio count is numeric.
- Removed duplicate records (if any).

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| Used for Analytics | Industry Growth Analysis |

---

# Dataset 7 : Scheme Performance

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 07_scheme_performance.csv |
| Purpose | Stores historical performance metrics of mutual fund schemes. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | amfi_code |
| Used In | fact_performance |
| Cleaning Required | Yes |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| amfi_code | Integer | Unique AMFI scheme identifier. |
| return_1yr_pct | Float | One-year annual return percentage. |
| return_3yr_pct | Float | Three-year annualized return percentage. |
| return_5yr_pct | Float | Five-year annualized return percentage. |
| benchmark_3yr_pct | Float | Three-year benchmark return percentage. |
| alpha | Float | Excess return generated above the benchmark. |
| beta | Float | Sensitivity of the fund relative to the market. |
| sharpe_ratio | Float | Risk-adjusted return measurement. |
| sortino_ratio | Float | Downside risk-adjusted return measurement. |
| std_dev_ann_pct | Float | Annualized standard deviation (volatility). |
| max_drawdown_pct | Float | Maximum percentage decline from peak value. |
| expense_ratio_pct | Float | Annual fund management expense ratio. |
| morningstar_rating | Integer | Morningstar rating assigned to the fund. |

---

## Business Rules

- Performance values must be numeric.
- Expense ratio should generally fall between **0.1% and 2.5%**.
- One performance record exists per mutual fund scheme.

---

## Cleaning Rules Applied

- Converted all return columns to numeric values.
- Flagged non-numeric performance values.
- Validated expense ratio range.
- Removed duplicate records (if any).

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| fact_performance | Stores scheme performance metrics |
| dim_fund | Connected using amfi_code |

---

# Dataset 8 : Investor Transactions

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 08_investor_transactions.csv |
| Purpose | Stores individual investor transaction records. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | transaction_id (Generated) |
| Used In | fact_transactions |
| Cleaning Required | Yes |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| investor_id | Text | Unique identifier of an investor. |
| amfi_code | Integer | Mutual fund scheme identifier. |
| transaction_date | Date | Date of transaction. |
| transaction_type | Text | Type of transaction (SIP, Lumpsum, Redemption). |
| amount_inr | Float | Transaction amount in Indian Rupees. |
| state | Text | Investor's state. |
| city | Text | Investor's city. |
| city_tier | Text | Classification of city (Tier-1, Tier-2, Tier-3). |
| age_group | Text | Investor age category. |
| gender | Text | Investor gender. |
| annual_income_lakh | Float | Annual income in Lakhs. |
| payment_mode | Text | Payment method used. |
| kyc_status | Text | KYC verification status. |

---

## Business Rules

- Transaction amount must always be positive.
- Transaction type must be SIP, Lumpsum or Redemption.
- KYC status must contain valid values only.
- Every transaction belongs to one mutual fund scheme.

---

## Cleaning Rules Applied

- Standardized transaction type values.
- Fixed date formats.
- Validated transaction amount greater than zero.
- Standardized KYC status values.
- Removed duplicate records.

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| fact_transactions | Stores investor transaction history |
| dim_fund | Connected using amfi_code |
| dim_date | Connected using date_id |

---

# Dataset 9 : Portfolio Holdings

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 09_portfolio_holdings.csv |
| Purpose | Stores portfolio allocation details of mutual fund schemes. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | (amfi_code + holding_name) |
| Used In | Portfolio Analysis |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| amfi_code | Integer | Mutual fund scheme identifier. |
| holding_name | Text | Name of the security held. |
| sector | Text | Industry sector of the holding. |
| allocation_pct | Float | Percentage allocation in the portfolio. |

---

## Business Rules

- Portfolio allocation percentages should be between **0 and 100**.
- One scheme can have multiple holdings.

---

## Cleaning Rules Applied

- Verified allocation percentages.
- Removed duplicate holdings.
- Standardized sector names.

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| Used for Portfolio Analysis | Portfolio Composition |

---

# Dataset 10 : Benchmark Indices

---

## Dataset Information

| Property | Details |
|----------|---------|
| Dataset Name | 10_benchmark_indices.csv |
| Purpose | Stores benchmark market index performance data. |
| Source | BlueStock Mutual Fund Dataset |
| Primary Key | (benchmark_name + date) |
| Used In | Performance Comparison |
| Cleaning Required | Minor |

---

## Column Dictionary

| Column Name | Data Type | Business Definition |
|-------------|-----------|---------------------|
| benchmark_name | Text | Name of the benchmark index. |
| date | Date | Reporting date. |
| index_value | Float | Closing value of the benchmark index. |

---

## Business Rules

- Benchmark values must be numeric.
- One value exists for each benchmark on each reporting date.

---

## Cleaning Rules Applied

- Converted date to DateTime format.
- Verified index values are numeric.
- Removed duplicate records.

---

## Database Mapping

| Database Table | Mapping |
|---------------|---------|
| Used for Performance Comparison | Benchmark Analysis |

---

# Data Quality Rules

---

The following data quality rules were applied throughout the ETL pipeline to ensure data consistency, integrity, and reliability.

| Dataset | Data Quality Rules Applied |
|----------|---------------------------|
| Fund Master | Verified unique AMFI codes, validated mandatory fields, preserved master metadata. |
| NAV History | Converted dates to DateTime, sorted records, forward-filled missing NAV values, removed duplicates, validated NAV > 0. |
| AUM by Fund House | Converted dates, validated numeric AUM values, removed duplicates, ensured AUM > 0. |
| Monthly SIP Inflows | Converted month to DateTime, validated numeric SIP inflow values, removed duplicates. |
| Category Inflows | Converted month to DateTime, validated numeric inflows, preserved valid negative outflows. |
| Industry Folio Count | Converted month to DateTime, validated folio counts, removed duplicates. |
| Scheme Performance | Converted return metrics to numeric, validated expense ratio (0.1%–2.5%), flagged anomalies, removed duplicates. |
| Investor Transactions | Standardized transaction types, validated transaction amount > 0, fixed date formats, standardized KYC values, removed duplicates. |
| Portfolio Holdings | Verified allocation percentages, standardized sector names, removed duplicate holdings. |
| Benchmark Indices | Converted dates to DateTime, validated numeric index values, removed duplicates. |

---

# Primary Keys

---

| Table | Primary Key |
|--------|-------------|
| dim_fund | amfi_code |
| dim_date | date_id |
| fact_nav | nav_id |
| fact_transactions | transaction_id |
| fact_performance | performance_id |
| fact_aum | aum_id |

---

# Foreign Keys

---

| Child Table | Foreign Key | Parent Table |
|--------------|-------------|--------------|
| fact_nav | amfi_code | dim_fund.amfi_code |
| fact_nav | date_id | dim_date.date_id |
| fact_transactions | amfi_code | dim_fund.amfi_code |
| fact_transactions | date_id | dim_date.date_id |
| fact_performance | amfi_code | dim_fund.amfi_code |
| fact_aum | date_id | dim_date.date_id |

---

# Source References

---

| Source | Description |
|----------|-------------|
| BlueStock Mutual Fund Dataset | Primary dataset used for this project. |
| AMFI (Association of Mutual Funds in India) | Standard AMFI Scheme Codes and Mutual Fund information. |
| MFAPI | Live Net Asset Value (NAV) data fetched through the MFAPI REST API. |
| SQLite | Relational database used for the Data Warehouse implementation. |
| Python (Pandas) | Data ingestion, cleaning, transformation and validation. |
| SQLAlchemy | ETL loading from Pandas DataFrames into SQLite. |

---

# Database Schema Summary

---

## Dimension Tables

- **dim_fund** : Stores master information of mutual fund schemes.
- **dim_date** : Stores calendar attributes for date-based analysis.

---

## Fact Tables

- **fact_nav** : Historical NAV values for mutual fund schemes.
- **fact_transactions** : Investor transaction records.
- **fact_performance** : Performance metrics of mutual fund schemes.
- **fact_aum** : Assets Under Management of fund houses.

---

# ETL Workflow Summary

---

The project follows a complete ETL (Extract, Transform, Load) pipeline.

### Extract

- Imported 10 CSV datasets.
- Retrieved live NAV data using the MFAPI.

### Transform

- Cleaned missing values.
- Standardized date formats.
- Removed duplicate records.
- Validated numeric fields.
- Standardized categorical values.
- Applied business validation rules.

### Load

- Designed a SQLite Star Schema.
- Loaded Dimension Tables.
- Loaded Fact Tables.
- Verified row counts after loading.

---

# Project Deliverables

---

The project successfully delivers:

- Raw Dataset Ingestion
- Data Cleaning Pipeline
- Data Validation
- Live NAV Integration
- SQLite Star Schema
- ETL Pipeline
- Analytical SQL Queries
- Data Dictionary
- GitHub Repository

---

# Conclusion

---

This Data Dictionary documents the structure, business meaning, relationships, and quality rules of every dataset used in the BlueStock Mutual Fund Analytics project.

It serves as the primary reference document for developers, analysts, and stakeholders working with the project database and ETL pipeline.

---