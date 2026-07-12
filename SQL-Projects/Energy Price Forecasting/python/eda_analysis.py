import pandas as pd
import pymysql
import matplotlib.pyplot as plt


# Database connection

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


print(df.head())

print(df.describe())