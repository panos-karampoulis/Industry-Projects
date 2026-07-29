from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "analytics"
)


PLOT_DIR = (
    DATA_DIR
    / "plots"
)

PLOT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# LOAD
# ==========================================================

balancing = pd.read_csv(
    DATA_DIR
    /
    "balancing_risk_ranking.csv"
)


price = pd.read_csv(
    DATA_DIR
    /
    "price_risk_ranking.csv"
)


renewable = pd.read_csv(
    DATA_DIR
    /
    "renewable_risk_ranking.csv"
)


summary = pd.read_csv(
    DATA_DIR
    /
    "country_risk_summary.csv"
)



# ==========================================================
# BALANCING RISK
# ==========================================================

plt.figure(
    figsize=(8,5)
)


sns.barplot(

    data=balancing,

    x="country",

    y="balancing_risk_score"

)


plt.title(
    "Balancing Risk Ranking"
)


plt.ylabel(
    "Risk Score"
)


plt.xlabel(
    ""
)


plt.tight_layout()


plt.savefig(
    PLOT_DIR
    /
    "balancing_risk.png",
    dpi=300
)


plt.close()



# ==========================================================
# PRICE RISK
# ==========================================================


plt.figure(
    figsize=(8,5)
)


sns.barplot(

    data=price,

    x="country",

    y="price_risk_score"

)


plt.title(
    "Electricity Price Risk Ranking"
)


plt.ylabel(
    "Risk Score"
)


plt.xlabel(
    ""
)


plt.tight_layout()


plt.savefig(
    PLOT_DIR
    /
    "price_risk.png",
    dpi=300
)


plt.close()



# ==========================================================
# RENEWABLE RISK
# ==========================================================


plt.figure(
    figsize=(8,5)
)


sns.barplot(

    data=renewable,

    x="country",

    y="renewable_risk_score"

)


plt.title(
    "Renewable Exposure Risk Ranking"
)


plt.ylabel(
    "Risk Score"
)


plt.xlabel(
    ""
)


plt.tight_layout()


plt.savefig(
    PLOT_DIR
    /
    "renewable_risk.png",
    dpi=300
)


plt.close()



# ==========================================================
# COUNTRY COMPARISON
# ==========================================================


comparison = summary[

    [

    "country",

    "imbalance_volatility_mw",

    "price_volatility",

    "renewable_share"

    ]

]


comparison = comparison.melt(

    id_vars="country",

    var_name="metric",

    value_name="value"

)


comparison["metric"] = comparison["metric"].replace(

    {
        "imbalance_volatility_mw": "Imbalance Volatility (MW)",
        "price_volatility": "Price Volatility",
        "renewable_share": "Renewable Share"
    }

)



plt.figure(
    figsize=(10,6)
)


sns.barplot(

    data=comparison,

    x="country",

    y="value",

    hue="metric"

)


plt.title(
    "European Market Risk Comparison"
)


plt.xlabel(
    ""
)


plt.tight_layout()


plt.savefig(

    PLOT_DIR
    /
    "country_comparison.png",

    dpi=300

)


plt.close()



print("="*70)
print("VISUALIZATION COMPLETED")
print("="*70)

print(
    "Saved plots:",
    PLOT_DIR
)