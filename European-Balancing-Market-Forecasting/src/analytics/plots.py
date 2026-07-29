import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


ANALYTICS_DIR = (
    BASE_DIR
    /
    "data"
    /
    "analytics"
)


PLOTS_DIR = (
    ANALYTICS_DIR
    /
    "plots"
)


PLOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# LOAD DATA
# ============================================================


price_summary = pd.read_csv(
    ANALYTICS_DIR
    /
    "price_summary.csv"
)


load_summary = pd.read_csv(
    ANALYTICS_DIR
    /
    "load_summary.csv"
)



# ============================================================
# 1. AVERAGE PRICE COMPARISON
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(
    price_summary["country"],
    price_summary["average_price"]
)


plt.title(
    "Average Day Ahead Electricity Price"
)


plt.ylabel(
    "EUR/MWh"
)


plt.xlabel(
    "Country"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(

    PLOTS_DIR
    /
    "average_prices.png",

    dpi=300

)


plt.close()



# ============================================================
# 2. NEGATIVE PRICE EVENTS
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(

    price_summary["country"],

    price_summary["negative_price_hours"]

)


plt.title(
    "Negative Price Events"
)


plt.ylabel(
    "Hours"
)


plt.xlabel(
    "Country"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(

    PLOTS_DIR
    /
    "negative_prices.png",

    dpi=300

)


plt.close()



# ============================================================
# 3. PRICE VOLATILITY
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(

    price_summary["country"],

    price_summary["price_std"]

)


plt.title(
    "Electricity Price Volatility"
)


plt.ylabel(
    "Standard Deviation EUR/MWh"
)


plt.xlabel(
    "Country"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(

    PLOTS_DIR
    /
    "price_volatility.png",

    dpi=300

)


plt.close()



# ============================================================
# 4. LOAD COMPARISON
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(

    load_summary["country"],

    load_summary["average_load_mw"]

)


plt.title(
    "Average Electricity Load"
)


plt.ylabel(
    "MW"
)


plt.xlabel(
    "Country"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(

    PLOTS_DIR
    /
    "average_load.png",

    dpi=300

)


plt.close()



print(
    "PLOTS GENERATED"
)


print(
    PLOTS_DIR
)