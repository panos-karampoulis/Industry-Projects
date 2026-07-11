import pandas as pd
from database import get_connection


views = [
    "vw_executive_dashboard",
    "vw_market_analysis",
    "vw_trader_performance",
    "vw_renewable_analysis"
]


connection = get_connection()


for view in views:

    query = f"SELECT * FROM {view} LIMIT 5"

    df = pd.read_sql(query, connection)

    print("\n======================")
    print(view)
    print("======================")

    print(df.columns.tolist())
    print(df.head())


connection.close()