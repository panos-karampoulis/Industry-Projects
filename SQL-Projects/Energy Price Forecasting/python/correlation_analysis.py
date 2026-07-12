import pandas as pd
import pymysql


connection = pymysql.connect(

    host="localhost",
    user="root",
    password="Econ12070",
    database="EnergyMarketForecasting"

)


query = """
SELECT *
FROM energy_prices;
"""


df = pd.read_sql(
    query,
    connection
)


connection.close()


correlation = df.corr(
    numeric_only=True
)


print(
    correlation["Electricity_Price_EUR"]
    .sort_values(
        ascending=False
    )
)