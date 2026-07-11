from database import get_connection
from report_generator import create_summary_report

import pandas as pd


query = """
SELECT *
FROM vw_executive_dashboard;
"""


connection = get_connection()

df = pd.read_sql(query, connection)

connection.close()


report = create_summary_report(df)


print(report)