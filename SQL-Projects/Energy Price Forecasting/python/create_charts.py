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


# Convert Date column

df["Date"] = pd.to_datetime(df["Date"])


# 1. Electricity Price Trend

plt.figure(figsize=(12,5))

plt.plot(
    df["Date"],
    df["Electricity_Price_EUR"]
)

plt.title("Electricity Price Trend")
plt.xlabel("Date")
plt.ylabel("Price €/MWh")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/price_trend.png")
plt.close()



# 2. Demand vs Price

plt.figure(figsize=(7,5))

plt.scatter(
    df["Demand_MWh"],
    df["Electricity_Price_EUR"]
)

plt.title("Demand vs Electricity Price")
plt.xlabel("Demand MWh")
plt.ylabel("Price €/MWh")

plt.tight_layout()

plt.savefig("charts/demand_price.png")
plt.close()



# 3. Renewable Impact

df["Renewable_Total_MWh"] = (
    df["Wind_Generation_MWh"]
    +
    df["Solar_Generation_MWh"]
)


plt.figure(figsize=(7,5))

plt.scatter(
    df["Renewable_Total_MWh"],
    df["Electricity_Price_EUR"]
)

plt.title("Renewable Generation vs Electricity Price")
plt.xlabel("Renewable Generation MWh")
plt.ylabel("Price €/MWh")

plt.tight_layout()

plt.savefig("charts/renewable_impact.png")
plt.close()