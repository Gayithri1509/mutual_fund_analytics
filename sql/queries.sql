-- 10 ANALYTICAL SQL QUERIES
-- Mutual Fund Analytics | Bluestock Fintech

-- Q1: Top 5 funds by AUM
SELECT fund_house, SUM(aum_crore) as total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

-- Q2: Average NAV per month
SELECT strftime('%Y-%m', date) as month,
       ROUND(AVG(nav), 2) as avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- Q3: SIP transactions by state
SELECT state, COUNT(*) as sip_count,
       ROUND(SUM(amount_inr), 2) as total_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY sip_count DESC;

-- Q4: Funds with expense ratio < 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Q5: Top 5 funds by 3yr return
SELECT scheme_name, fund_house, return_3yr_pct
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- Q6: Transaction count by type
SELECT transaction_type,
       COUNT(*) as count,
       ROUND(SUM(amount_inr), 2) as total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- Q7: KYC status distribution
SELECT kyc_status, COUNT(*) as count
FROM fact_transactions
GROUP BY kyc_status;

-- Q8: Gender wise investment
SELECT gender,
       COUNT(*) as transactions,
       ROUND(AVG(amount_inr), 2) as avg_amount
FROM fact_transactions
GROUP BY gender;

-- Q9: Top 5 funds by 1yr return
SELECT scheme_name, return_1yr_pct, risk_grade
FROM fact_performance fp
JOIN dim_fund df ON fp.amfi_code = df.amfi_code
ORDER BY return_1yr_pct DESC
LIMIT 5;

-- Q10: Monthly SIP growth trend
SELECT strftime('%Y-%m', transaction_date) as month,
       COUNT(*) as sip_count,
       ROUND(SUM(amount_inr), 2) as total_sip
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY month
ORDER BY month;