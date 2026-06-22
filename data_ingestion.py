import pandas as pd
import requests
import os
import json
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
        print(f"✅ Saved: {filename}")
        print(f"   Shape: {nav_df.shape}")
        print(f"   Date range: {nav_df['date'].min()} → {nav_df['date'].max()}")
        print(f"   Latest NAV: ₹{nav_df['nav'].iloc[-1]}")
        
        return nav_df
    
    except Exception as e:
        print(f"❌ Error fetching {scheme_name}: {e}")
        return None


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
        print(f"\n✅ Combined file saved!")
        print(f"   Total records: {len(combined)}")
        print(f"   Schemes: {combined['scheme_name'].unique()}")
    
    print("\n✅ Data Ingestion Complete!")

if __name__ == "__main__":
    main()