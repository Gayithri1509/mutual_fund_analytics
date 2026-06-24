import pandas as pd
import numpy as np
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


def clean_nav_history():
    print("\n== Cleaning nav_history.csv ==")
    df = pd.read_csv(f"{RAW_DIR}/02_nav_history.csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['amfi_code', 'date'])
    df = df.drop_duplicates()
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df[df['nav'] > 0]
    df['nav'] = df.groupby('amfi_code')['nav'].ffill()
    df.to_csv(f"{PROCESSED_DIR}/nav_history_clean.csv", index=False)
    print(f"Done | Shape: {df.shape} | Nulls: {df.isnull().sum().sum()}")
    return df


def clean_investor_transactions():
    print("\n== Cleaning investor_transactions.csv ==")
    df = pd.read_csv(f"{RAW_DIR}/08_investor_transactions.csv")
    df['transaction_type'] = df['transaction_type'].str.strip().str.title()
    df['transaction_type'] = df['transaction_type'].replace({
        'Sip': 'SIP', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption'
    })
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df = df[df['amount_inr'] > 0]
    df['kyc_status'] = df['kyc_status'].str.strip().str.upper()
    df.to_csv(f"{PROCESSED_DIR}/investor_transactions_clean.csv", index=False)
    print(f" Done | Shape: {df.shape} | Nulls: {df.isnull().sum().sum()}")
    return df


def clean_scheme_performance():
    print("\n== Cleaning scheme_performance.csv ==")
    df = pd.read_csv(f"{RAW_DIR}/07_scheme_performance.csv")
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
    for col in return_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'expense_ratio' in df.columns:
        df['expense_ratio'] = pd.to_numeric(df['expense_ratio'], errors='coerce')
        anomalies = df[(df['expense_ratio'] < 0.1) | (df['expense_ratio'] > 2.5)]
        print(f"   Expense ratio anomalies: {len(anomalies)}")
    df.to_csv(f"{PROCESSED_DIR}/scheme_performance_clean.csv", index=False)
    print(f"Done | Shape: {df.shape} | Nulls: {df.isnull().sum().sum()}")
    return df


def main():
    print("=" * 55)
    print("  DAY 2 — DATA CLEANING")
    print("=" * 55)
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    print("\n✅ All cleaning complete!")

if __name__ == "__main__":
    main()