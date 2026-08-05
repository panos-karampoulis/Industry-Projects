from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]


RESULTS = BASE_DIR / "results"
FEATURES = BASE_DIR / "data" / "features"
SAMPLE = BASE_DIR / "data" / "sample"


SAMPLE.mkdir(
    exist_ok=True
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


# =====================================================
# FEATURES
# =====================================================

for country in COUNTRIES:

    file = FEATURES / f"{country}_features.csv"

    df = pd.read_csv(file)

    sample = (
        df
        .tail(5000)
        .copy()
    )


    output = (
        SAMPLE /
        f"{country}_features_sample.csv"
    )


    sample.to_csv(
        output,
        index=False
    )


    print(
        "Saved:",
        output
    )



# =====================================================
# RISK
# =====================================================

risk = pd.read_csv(
    RESULTS /
    "all_countries_imbalance_risk.csv"
)


risk_sample = (
    risk
    .groupby("country")
    .tail(5000)
)


risk_sample.to_csv(
    SAMPLE /
    "imbalance_risk_sample.csv",
    index=False
)


print(
    "Risk sample saved"
)



# =====================================================
# TRADING
# =====================================================

trade = pd.read_csv(
    RESULTS /
    "trading_decisions_all_countries.csv"
)


trade_sample = (
    trade
    .groupby("country")
    .tail(5000)
)


trade_sample.to_csv(
    SAMPLE /
    "trading_decisions_sample.csv",
    index=False
)


print(
    "Trading sample saved"
)