import requests
import json
import csv
import os
from datetime import datetime

# ── Config ────────────────────────────────────────────────
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# HDFC Top 100 Direct — scheme code 125497
HDFC_CODE = "125497"

# ── Fetch Live NAV ────────────────────────────────────────
def fetch_live_nav(scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"\nFetching live NAV for scheme: {scheme_code}...")

    try:
        response = requests.get(url, timeout=60)
        data = response.json()

        meta = data["meta"]
        latest = data["data"][0]  # Most recent NAV

        print("\n── Scheme Details ──────────────────────")
        print(f"  Fund House : {meta['fund_house']}")
        print(f"  Scheme     : {meta['scheme_name']}")
        print(f"  Category   : {meta['scheme_category']}")
        print(f"  Type       : {meta['scheme_type']}")
        print(f"  Date       : {latest['date']}")
        print(f"  NAV        : ₹{latest['nav']}")
        print("────────────────────────────────────────")

        return data

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ── Save as CSV ───────────────────────────────────────────
def save_to_csv(data, scheme_code):
    if not data:
        return

    filename = f"{RAW_DIR}/hdfc_top100_nav.csv"
    nav_records = data["data"]
    meta = data["meta"]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "nav", "scheme_name",
                         "fund_house", "scheme_code"])
        for record in nav_records:
            writer.writerow([
                record["date"],
                record["nav"],
                meta["scheme_name"],
                meta["fund_house"],
                scheme_code
            ])

    print(f"\n✅ Saved: {filename}")
    print(f"   Total records: {len(nav_records)}")

# ── Main ──────────────────────────────────────────────────
def main():
    print("=" * 45)
    print("  LIVE NAV FETCH — HDFC Top 100 Direct")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    data = fetch_live_nav(HDFC_CODE)
    save_to_csv(data, HDFC_CODE)

    print("\n✅ Live NAV Fetch Complete!")

if __name__ == "__main__":
    main()
    