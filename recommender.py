# recommender.py
import pandas as pd
import sqlite3

DB_PATH = r'C:\Users\gayat\OneDrive\Documents\mutual_fund_analytics\bluestock_mf.db'
PROCESSED_PATH = r'C:\Users\gayat\OneDrive\Documents\mutual_fund_analytics\data\processed'

def recommend_funds(risk_appetite):
    risk_map = {
        'Low':      ['Low', 'Moderately Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High':     ['High', 'Very High']
    }

    conn = sqlite3.connect(DB_PATH)
    fund_df = pd.read_sql("SELECT * FROM dim_fund", conn)
    conn.close()

    # Check available columns
    print("Fund columns:", fund_df.columns.tolist())

    scorecard = pd.read_csv(f'{PROCESSED_PATH}/fund_scorecard.csv')
    
    # Use risk_grade from scorecard if available
    if 'risk_grade' in scorecard.columns:
        merged = scorecard
    elif 'risk_grade' in fund_df.columns:
        merged = scorecard.merge(
            fund_df[['amfi_code','risk_grade']], 
            on='amfi_code', how='left'
        )
    else:
        # No risk_grade — use fund_score ranking only
        print(f"\n🎯 Top 3 Recommendations — {risk_appetite} Risk:")
        top3 = scorecard.nlargest(3, 'sharpe_ratio')[
            ['scheme_name','sharpe_ratio','cagr_3yr','fund_score']
        ]
        print(top3.to_string(index=False))
        return top3

    grades = risk_map.get(risk_appetite, ['Moderate'])
    filtered = merged[merged['risk_grade'].isin(grades)] if 'risk_grade' in merged.columns else merged
    top3 = filtered.nlargest(3, 'sharpe_ratio')[
        ['scheme_name','sharpe_ratio','cagr_3yr','fund_score']
    ]
    print(f"\n🎯 Top 3 Recommendations — {risk_appetite} Risk:")
    print("=" * 60)
    print(top3.to_string(index=False))
    return top3

if __name__ == "__main__":
    for risk in ['Low', 'Moderate', 'High']:
        recommend_funds(risk)