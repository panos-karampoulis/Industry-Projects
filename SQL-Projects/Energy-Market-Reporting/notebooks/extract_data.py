import pandas as pd
from database import get_connection


query = """
SELECT *
FROM vw_executive_dashboard;
"""


connection = get_connection()


df = pd.read_sql(query, connection)


connection.close()


print(df.head())

print("\nRows:", len(df))