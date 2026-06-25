-- ==========================================================
-- BlueStock Mutual Fund Analytics
-- Analytical SQL Queries
-- ==========================================================

-- ==========================================================
-- Query 1 : Top 5 Funds by AUM
-- ==========================================================

SELECT
    fund_house,
    aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;


-- ==========================================================
-- Query 2 : Average NAV Per Month
-- ==========================================================

SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
JOIN dim_date d
ON n.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ==========================================================
-- Query 3 : SIP Year-over-Year Growth
-- ==========================================================

SELECT
    d.year,
    ROUND(SUM(t.amount_inr), 2) AS total_sip
FROM fact_transactions t
JOIN dim_date d
ON t.date_id = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;


-- ==========================================================
-- Query 4 : Transactions by State
-- ==========================================================

SELECT
    state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- ==========================================================
-- Query 5 : Funds with Expense Ratio Below 1%
-- ==========================================================

SELECT
    f.scheme_name,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;


-- ==========================================================
-- Query 6 : Top 10 Funds by 5-Year Return
-- ==========================================================

SELECT
    f.scheme_name,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code = f.amfi_code
ORDER BY p.return_5yr_pct DESC
LIMIT 10;


-- ==========================================================
-- Query 7 : Average Investment Amount by Transaction Type
-- ==========================================================

SELECT
    transaction_type,
    ROUND(AVG(amount_inr), 2) AS average_amount
FROM fact_transactions
GROUP BY transaction_type;


-- ==========================================================
-- Query 8 : Number of Funds in Each Category
-- ==========================================================

SELECT
    category,
    COUNT(*) AS total_funds
FROM dim_fund
GROUP BY category
ORDER BY total_funds DESC;


-- ==========================================================
-- Query 9 : Fund Houses with Most Schemes
-- ==========================================================

SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;


-- ==========================================================
-- Query 10 : Highest Sharpe Ratio Funds
-- ==========================================================

SELECT
    f.scheme_name,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 10;