import numpy as np
import pandas as pd

# Για να παίρνουμε πάντα τα ίδια αποτελέσματα
np.random.seed(42)

# Δημιουργία 2 ετών ημερήσιων δεδομένων
dates = pd.date_range(
    start="2023-01-01",
    end="2024-12-31",
    freq="D"
)

df = pd.DataFrame({
    "Date": dates
})

print(df.head())
print(df.tail())
print(f"Rows: {len(df)}")


# Demand (MWh)
df["Demand_MWh"] = (
    35000
    + 5000 * np.sin(np.arange(len(df)) * 2 * np.pi / 365)
    + np.random.normal(0, 1200, len(df))
)


# Wind generation (MWh)
df["Wind_Generation_MWh"] = (
    7000
    + 2000 * np.sin(np.arange(len(df)) * 2 * np.pi / 180)
    + np.random.normal(0, 800, len(df))
)


# Solar generation (MWh)
df["Solar_Generation_MWh"] = np.maximum(
    0,
    (
        5000 * np.sin(np.arange(len(df)) * 2 * np.pi / 365)
        + np.random.normal(0, 300, len(df))
    )
)

# Electricity price €/MWh

renewable_generation = (
    df["Wind_Generation_MWh"]
    + df["Solar_Generation_MWh"]
)




# Natural Gas price €/MWh
df["Gas_Price_EUR"] = (
    40
    + 5 * np.sin(np.arange(len(df)) * 2 * np.pi / 365)
    + np.random.normal(0, 2, len(df))
)


# CO2 price €/ton
df["CO2_Price_EUR"] = (
    80
    + 10 * np.sin(np.arange(len(df)) * 2 * np.pi / 365)
    + np.random.normal(0, 3, len(df))
)


# Temperature Celsius
df["Temperature_C"] = (
    15
    + 10 * np.sin(np.arange(len(df)) * 2 * np.pi / 365)
    + np.random.normal(0, 2, len(df))
)

# Electricity price €/MWh

renewable_generation = (
    df["Wind_Generation_MWh"]
    + df["Solar_Generation_MWh"]
)

df["Electricity_Price_EUR"] = (
    40
    + 0.0015 * df["Demand_MWh"]
    + 0.8 * df["Gas_Price_EUR"]
    + 0.35 * df["CO2_Price_EUR"]
    - 0.001 * renewable_generation
    + np.random.normal(0, 5, len(df))
)

print(df.head())
print(df.describe())

# Save dataset

output_file = "data/energy_market_prices.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"Dataset saved successfully: {output_file}")