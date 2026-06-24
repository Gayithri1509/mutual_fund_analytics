# Data Dictionary — Mutual Fund Analytics

## 1. dim_fund
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Unique fund identifier |
| scheme_name | TEXT | Full name of the scheme |
| fund_house | TEXT | Asset Management Company |
| category | TEXT | Equity / Debt |
| sub_category | TEXT | Large Cap / Small Cap etc |
| plan | TEXT | Regular / Direct |
| risk_grade | TEXT | Low / Moderate / High |
| expense_ratio_pct | REAL | Annual fee percentage |

## 2. fact_nav
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Fund identifier |
| date | TEXT | NAV date |
| nav | REAL | Net Asset Value in ₹ |

## 3. fact_transactions
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID |
| amfi_code | TEXT | Fund identifier |
| transaction_date | TEXT | Date of transaction |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Transaction amount in ₹ |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| gender | TEXT | M / F |
| kyc_status | TEXT | KYC / NON-KYC |

## 4. fact_performance
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Fund identifier |
| return_1yr_pct | REAL | 1 year return % |
| return_3yr_pct | REAL | 3 year return % |
| return_5yr_pct | REAL | 5 year return % |
| sharpe_ratio | REAL | Risk adjusted return |
| alpha | REAL | Excess return vs benchmark |
| beta | REAL | Market sensitivity |

## 5. fact_aum
| Column | Type | Description |
|--------|------|-------------|
| fund_house | TEXT | AMC name |
| month | TEXT | Month of AUM |
| aum_crore | REAL | Assets Under Management |

## Sources
- mfapi.in — Live NAV API
- Bluestock Fintech — Provided datasets