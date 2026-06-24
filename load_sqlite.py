import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine

DB_PATH = "bluestock_mf.db"
PROCESSED_DIR = "data/processed"
RAW_DIR = "data/raw"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Database created!")

def load_data():
    engine = create_engine(f"sqlite:///{DB_PATH}")

    # dim_fund
    df = pd.read_csv(f"{RAW_DIR}/01_fund_master.csv")
    df.to_sql("dim_fund", engine, if_exists="replace", index=False)
    print(f"✅ dim_fund: {len(df)} rows")

    # fact_nav
    df = pd.read_csv(f"{PROCESSED_DIR}/nav_history_clean.csv")
    df.to_sql("fact_nav", engine, if_exists="replace", index=False)
    print(f"✅ fact_nav: {len(df)} rows")

    # fact_transactions
    df = pd.read_csv(f"{PROCESSED_DIR}/investor_transactions_clean.csv")
    df.to_sql("fact_transactions", engine, if_exists="replace", index=False)
    print(f"✅ fact_transactions: {len(df)} rows")

    # fact_performance
    df = pd.read_csv(f"{PROCESSED_DIR}/scheme_performance_clean.csv")
    df.to_sql("fact_performance", engine, if_exists="replace", index=False)
    print(f"✅ fact_performance: {len(df)} rows")

    # fact_aum
    df = pd.read_csv(f"{RAW_DIR}/03_aum_by_fund_house.csv")
    df.to_sql("fact_aum", engine, if_exists="replace", index=False)
    print(f"✅ fact_aum: {len(df)} rows")

def verify():
    conn = sqlite3.connect(DB_PATH)
    tables = ["dim_fund", "fact_nav", "fact_transactions",
              "fact_performance", "fact_aum"]
    print("\n── Row counts ──")
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {count}")
    conn.close()

def main():
    print("=" * 55)
    print("  DAY 2 — SQLITE DATABASE LOADING")
    print("=" * 55)
    create_database()
    load_data()
    verify()
    print("\n✅ SQLite DB ready!")

if __name__ == "__main__":
    main()