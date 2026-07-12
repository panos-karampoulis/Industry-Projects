import pandas as pd
import pymysql


# Load dataset

df = pd.read_csv(
    "data/energy_market_prices.csv"
)


print("Dataset loaded")
print(df.head())


# MySQL connection

connection = pymysql.connect(

    host="localhost",
    user="root",
    password="Econ12070",
    database="EnergyMarketForecasting"

)


cursor = connection.cursor()


print("Connected successfully")


# Insert data

insert_query = """
INSERT INTO energy_prices
(
Date,
Demand_MWh,
Wind_Generation_MWh,
Solar_Generation_MWh,
Gas_Price_EUR,
CO2_Price_EUR,
Temperature_C,
Electricity_Price_EUR
)

VALUES
(%s,%s,%s,%s,%s,%s,%s,%s)

"""


for _, row in df.iterrows():

    cursor.execute(
        insert_query,
        (
            row["Date"],
            row["Demand_MWh"],
            row["Wind_Generation_MWh"],
            row["Solar_Generation_MWh"],
            row["Gas_Price_EUR"],
            row["CO2_Price_EUR"],
            row["Temperature_C"],
            row["Electricity_Price_EUR"]
        )
    )


connection.commit()


print("Data inserted successfully")


cursor.close()
connection.close()