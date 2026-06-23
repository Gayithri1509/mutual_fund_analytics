import pandas as pd
import requests
import os
from datetime import datetime

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

SCHEMES = {
    "SBI_Bluechip":     "119551",
    "ICICI_Bluechip":   "120503",
    "Nippon_LargeCap":  "118632",
    "Axis_Bluechip":    "119092",
    "Kotak_Bluechip":   "120841"
}

def fetch_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"\nFetching: {scheme_name} ({scheme_code})...")
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        nav_df = pd.DataFrame(data["data"])
        nav_df["scheme_name"] = scheme_name
        nav_df["scheme_code"] = scheme_code
        nav_df["date"] = pd.to_datetime(nav_df["date"], format="%d-%m-%Y")
        nav_df["nav"] = pd.to_numeric(nav_df["nav"])
        nav_df = nav_df.sort_values("date")
        filename = f"{RAW_DIR}/{scheme_name}_nav.csv"
        nav_df.to_csv(filename, index=False)
        print(f"✅ Saved: {filename} | Shape: {nav_df.shape}")
        return nav_df
    except Exception as e:
        print(f" Error fetching {scheme_name}: {e}")
        return None

def load_bluestock_csvs():
    print("\n" + "=" * 55)
    print("  LOADING BLUESTOCK PROVIDED DATASETS")
    print("=" * 55)
    files = [
        "01_fund_master", "02_nav_history", "03_aum_by_fund_house",
        "04_monthly_sip_inflows", "05_category_inflows",
        "06_industry_folio_count", "07_scheme_performance",
        "08_investor_transactions", "09_portfolio_holdings",
        "10_benchmark_indices"
    ]
    for f in files:
        path = f"data/raw/{f}.csv"
        try:
            df = pd.read_csv(path)
            print(f"✅ {f} | Shape: {df.shape}")
        except Exception as e:
            print(f"{f}: {e}")

def explore_fund_master():
    print("\n" + "=" * 55)
    print("  FUND MASTER EXPLORATION")
    print("=" * 55)
    try:
        df = pd.read_csv("data/raw/01_fund_master.csv")
        print(f"\nUnique Fund Houses ({df['fund_house'].nunique()}):")
        print(df['fund_house'].unique())
        print(f"\nUnique Categories ({df['category'].nunique()}):")
        print(df['category'].unique())
        if 'risk_grade' in df.columns:
            print(f"\nRisk Grades: {df['risk_grade'].unique()}")
    except Exception as e:
        print(f" Error: {e}")

def validate_amfi_codes():
    print("\n" + "=" * 55)
    print("  AMFI CODE VALIDATION")
    print("=" * 55)
    try:
        fund_master = pd.read_csv("data/raw/01_fund_master.csv")
        nav_history = pd.read_csv("data/raw/02_nav_history.csv")
        master_codes = set(fund_master['amfi_code'].astype(str))
        nav_codes = set(nav_history['amfi_code'].astype(str))
        missing = master_codes - nav_codes
        print(f"\nFund master codes : {len(master_codes)}")
        print(f"Nav history codes : {len(nav_codes)}")
        print(f"Missing in nav    : {len(missing)}")
        if missing:
            print(f"Missing codes: {missing}")
        else:
            print("✅ All AMFI codes validated!")
    except Exception as e:
        print(f" Error: {e}")

def data_quality_summary():
    print("\n" + "=" * 55)
    print("  DATA QUALITY SUMMARY")
    print("=" * 55)
    files = {
        "fund_master": "01_fund_master.csv",
        "nav_history": "02_nav_history.csv",
        "investor_transactions": "08_investor_transactions.csv"
    }
    for name, file in files.items():
        try:
            df = pd.read_csv(f"data/raw/{file}")
            nulls = df.isnull().sum().sum()
            print(f"\n{name}: {df.shape} | Nulls: {nulls}")
        except Exception as e:
            print(f"{name}: {e}")
    print("\n✅ Data Quality Check Complete!")

def main():
    print("=" * 55)
    print("  MUTUAL FUND DATA INGESTION — mfapi.in")
    print(f"  Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)
    all_data = []
    for name, code in SCHEMES.items():
        df = fetch_nav(name, code)
        if df is not None:
            all_data.append(df)
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_csv(f"{PROCESSED_DIR}/all_schemes_nav.csv", index=False)
        print(f"\n✅ Combined file saved! Total records: {len(combined)}")
    print("\n✅ Data Ingestion Complete!")
    load_bluestock_csvs()
    explore_fund_master()
    validate_amfi_codes()
    data_quality_summary()

if __name__ == "__main__":
    main()