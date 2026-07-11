import matplotlib.pyplot as plt
import pandas as pd

from database import get_engine


engine = get_engine()


query = """
SELECT *
FROM vw_market_analysis
"""


df = pd.read_sql(query, engine)


plt.figure(figsize=(10,5))

plt.bar(
    df["market_name"],
    df["total_volume_mwh"]
)

plt.xticks(rotation=45)

plt.title("Trading Volume by Market")

plt.xlabel("Market")

plt.ylabel("Volume MWh")


plt.tight_layout()


plt.savefig(
    "charts/market_volume.png"
)


plt.close()


print("Market volume chart created")


# Trader P&L Chart

query = """
SELECT *
FROM vw_trader_performance
"""

df = pd.read_sql(query, engine)


df_sorted = df.sort_values(
    "pnl",
    ascending=False
)


plt.figure(figsize=(10,5))


plt.bar(
    df_sorted["trader_name"],
    df_sorted["pnl"]
)


plt.xticks(rotation=45)


plt.title("Trader Performance - P&L")


plt.xlabel("Trader")

plt.ylabel("P&L (€)")


plt.tight_layout()


plt.savefig(
    "charts/trader_pnl.png"
)


plt.close()


print("Trader P&L chart created")


# Renewable Mix Chart

query = """
SELECT *
FROM vw_renewable_analysis
"""

df = pd.read_sql(query, engine)


plt.figure(figsize=(7,7))


plt.pie(
    df["traded_volume"],
    labels=df["energy_type"],
    autopct="%1.1f%%"
)


plt.title("Renewable vs Non Renewable Trading Volume")


plt.tight_layout()


plt.savefig(
    "charts/renewable_mix.png"
)


plt.close()


print("Renewable mix chart created")