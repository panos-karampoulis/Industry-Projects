import os
import pandas as pd
import numpy as np


# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = r"D:\Portfolio\Energy-Trading-Decision-Support-System"


FEATURE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "features",
    "final"
)


SIGNAL_DIR = os.path.join(
    BASE_DIR,
    "data",
    "signals"
)


os.makedirs(
    SIGNAL_DIR,
    exist_ok=True
)


COUNTRIES = [
    "germany",
    "france",
    "netherlands",
    "spain",
    "italy"
]



# ==========================================================
# MARKET REGIME
# ==========================================================

def classify_market(row):

    price = row["price_eur_mwh"]

    volatility = row["volatility"]

    renewable = row["renewable_generation"]


    if price < 0:
        return "NEGATIVE_PRICE"


    if volatility > row["volatility_threshold"]:
        return "HIGH_VOLATILITY"


    if price > (
        row["rolling_mean_24h"]
        +
        2 * row["rolling_std_24h"]
    ):
        return "PRICE_SPIKE"


    if renewable > row["renewable_generation_rolling_mean"]:
        return "RENEWABLE_SURPLUS"


    return "NORMAL"



# ==========================================================
# RISK SCORE
# ==========================================================

def calculate_risk_score(row):

    score = 0


    # volatility
    if row["volatility"] > row["volatility_threshold"]:
        score += 30


    # price spikes
    if row["price_spike_flag"] == 1:
        score += 30


    # negative prices
    if row["negative_price_flag"] == 1:
        score += 20


    # low renewable availability
    if row["renewable_generation"] < (
        row["renewable_generation_rolling_mean"]
    ):
        score += 20


    return min(score,100)



# ==========================================================
# TRADING SIGNAL
# ==========================================================

def generate_signal(row):


    price = row["price_eur_mwh"]


    if (
        price < row["rolling_mean_24h"]
        and
        row["renewable_generation"] >
        row["renewable_generation_rolling_mean"]
        and
        row["volatility"] <
        row["volatility_threshold"]
    ):

        return "BUY"



    if (
        row["price_spike_flag"] == 1
        or
        row["volatility"] >
        row["volatility_threshold"]
    ):

        return "SELL"



    return "HOLD"



# ==========================================================
# PROCESS COUNTRY
# ==========================================================

def process_country(country):


    print("\n" + "="*60)
    print(country.upper())
    print("="*60)



    file_path = os.path.join(
        FEATURE_DIR,
        f"{country}_features_risk_final.csv"
    )


    if not os.path.exists(file_path):

        print("Missing file:")
        print(file_path)
        return



    df = pd.read_csv(
        file_path,
        index_col=0,
        parse_dates=True
    )


    df.index.name = "timestamp"



    print("Input shape:")
    print(df.shape)

    # ==================================================
    # FEATURE NAME COMPATIBILITY LAYER
    # ==================================================

    # Price

    if "day_ahead_price" in df.columns:
        df["price_eur_mwh"] = df["day_ahead_price"]


    # Volatility

    if "price_volatility_24h" in df.columns:
        df["volatility"] = df["price_volatility_24h"]


    # Rolling mean

    if "day_ahead_price_rolling_mean_24" in df.columns:
        df["rolling_mean_24h"] = (
            df["day_ahead_price_rolling_mean_24"]
        )


    # Rolling std

    if "day_ahead_price_rolling_std_24" in df.columns:
        df["rolling_std_24h"] = (
            df["day_ahead_price_rolling_std_24"]
        )


    # Price spike flag

    if "price_spike" in df.columns:
        df["price_spike_flag"] = df["price_spike"]

    elif "price_spike_flag" not in df.columns:
        df["price_spike_flag"] = 0


    # Negative prices

    if "negative_price_flag" not in df.columns:
        df["negative_price_flag"] = (
            df["price_eur_mwh"] < 0
        ).astype(int)
    # ==================================================
    # FEATURE PREPARATION
    # ==================================================

    df["volatility_threshold"] = (
        df["volatility"]
        .quantile(0.90)
    )



    df["renewable_generation_rolling_mean"] = (
        df["renewable_generation"]
        .rolling(
            window=96,
            min_periods=1
        )
        .mean()
    )



    # ==================================================
    # SIGNAL ENGINE
    # ==================================================

    df["market_regime"] = df.apply(
        classify_market,
        axis=1
    )


    df["risk_score"] = df.apply(
        calculate_risk_score,
        axis=1
    )


    df["trading_signal"] = df.apply(
        generate_signal,
        axis=1
    )



    # ==================================================
    # SAVE
    # ==================================================

    output = os.path.join(
        SIGNAL_DIR,
        f"{country}_trading_signals.csv"
    )


    df.to_csv(output)



    print("Saved:")
    print(output)


    print("\nSignal distribution:")

    print(
        df["trading_signal"]
        .value_counts()
    )


    print("\nAverage risk score:")

    print(
        round(
            df["risk_score"].mean(),
            2
        )
    )



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    print("="*70)
    print("ENERGY TRADING DECISION ENGINE")
    print("="*70)



    for country in COUNTRIES:

        process_country(country)



    print("\n")
    print("="*70)
    print("TRADING ENGINE COMPLETED")
    print("="*70)