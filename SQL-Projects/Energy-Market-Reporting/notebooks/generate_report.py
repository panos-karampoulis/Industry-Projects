import pandas as pd
from database import get_engine


engine = get_engine()


queries = {

    "Executive Summary": """
        SELECT *
        FROM vw_executive_dashboard
    """,

    "Market Analysis": """
        SELECT *
        FROM vw_market_analysis
    """,

    "Trader Performance": """
        SELECT *
        FROM vw_trader_performance
    """,

    "Renewable Analysis": """
        SELECT *
        FROM vw_renewable_analysis
    """
}


output_file = "reports/Energy_Market_Report_2025.xlsx"


with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for sheet_name, query in queries.items():

        df = pd.read_sql(query, engine)

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )




print("Excel report created successfully")