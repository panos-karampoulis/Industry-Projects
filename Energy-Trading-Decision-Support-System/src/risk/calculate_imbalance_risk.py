import pandas as pd
import joblib
import os


# =====================================================
# CONFIGURATION
# =====================================================

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


# =====================================================
# RISK CLASSIFICATION
# =====================================================

def classify_risk(score):

    if pd.isna(score):
        return "UNKNOWN"


    if score < 20:
        return "LOW"


    elif score < 40:
        return "MEDIUM"


    elif score < 70:
        return "HIGH"


    else:
        return "EXTREME"

# =====================================================
# LOAD MODEL
# =====================================================

def load_model(country):

    model_path = (
        f"models/{country}/{country}_load_forecaster.pkl"
    )

    features_path = (
        f"models/{country}/{country}_load_features.pkl"
    )


    model = joblib.load(
        model_path
    )

    features = joblib.load(
        features_path
    )


    return model, features



# =====================================================
# FEATURE PREPARATION
# =====================================================

def prepare_features(df, trained_features):


    X = df.drop(
        columns=[
            "load_mw",
            "timestamp",
            "Unnamed: 0"
        ],
        errors="ignore"
    )


    categorical_cols = X.select_dtypes(
        include=["object", "string"]
    ).columns


    X = pd.get_dummies(
        X,
        columns=categorical_cols,
        drop_first=True
    )


    # Align with training dataset

    X = X.reindex(
        columns=trained_features,
        fill_value=0
    )


    return X



# =====================================================
# RISK CALCULATION
# =====================================================

def calculate_risk(df):


    # ------------------------------
    # Imbalance
    # ------------------------------

    df["imbalance_mw"] = (
        df["load_mw"]
        -
        df["forecast_load_mw"]
    )


    df["imbalance_abs"] = (
        df["imbalance_mw"]
        .abs()
    )


    # ------------------------------
    # Imbalance Risk
    # ------------------------------

    imbalance_risk = (

        df["imbalance_abs"]

        /

        df["load_mw"]

        *

        100

    )


    # ------------------------------
    # Price Volatility Risk
    # ------------------------------

    price_max = (
        df["price_volatility_24h"]
        .max()
    )


    if price_max == 0:

        price_risk = 0

    else:

        price_risk = (

            df["price_volatility_24h"]

            /

            price_max

            *

            100

        )


    # ------------------------------
    # Renewable Risk
    # ------------------------------

    renewable_risk = (

        1

        -

        df["renewable_share"]

    ) * 100



    # ------------------------------
    # Final Risk Score
    # ------------------------------

    df["risk_score"] = (

        0.5 * imbalance_risk

        +

        0.25 * price_risk

        +

        0.25 * renewable_risk

    )


    # Keep values realistic

    df["risk_score"] = (

        df["risk_score"]
        .clip(0,100)

    )

    df["risk_score"] = (
        df["risk_score"]
        .fillna(0)
    )
    # Classification

    df["risk_level"] = (

        df["risk_score"]
        .apply(classify_risk)

    )


    # Backwards compatibility

    df["high_risk_event"] = (

        df["risk_level"]
        .isin(
            [
                "HIGH",
                "EXTREME"
            ]
        )

    )


    return df



# =====================================================
# COUNTRY PIPELINE
# =====================================================

def process_country(country):


    print("\n")
    print("="*60)
    print(
        f"CALCULATING IMBALANCE RISK: {country.upper()}"
    )
    print("="*60)



    feature_path = (

        f"data/features/{country}_features.csv"

    )


    output_path = (

        f"data/risk/{country}_imbalance_risk.csv"

    )



    print("Loading data...")


    df = pd.read_csv(
        feature_path
    )


    # Remove infinite values
    df = df.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )


    # Fill missing numeric values
    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns


    df[numeric_cols] = (
        df[numeric_cols]
        .fillna(
            df[numeric_cols].median()
        )
    )

    print(
        "Dataset:",
        df.shape
    )


    df.rename(
        columns={
            "Unnamed: 0":"timestamp"
        },
        inplace=True
    )



    model, trained_features = load_model(
        country
    )



    X = prepare_features(
        df,
        trained_features
    )


    print(
        "Generating load forecast..."
    )


    df["forecast_load_mw"] = (
        model.predict(X)
    )



    df = calculate_risk(
        df
    )



    os.makedirs(
        "data/risk",
        exist_ok=True
    )



    df.to_csv(
        output_path,
        index=False
    )


    print(
        "Saved:"
    )

    print(
        output_path
    )


    print(
        df[
            [
                "imbalance_mw",
                "risk_score",
                "risk_level",
                "high_risk_event"
            ]
        ]
        .head()
    )



# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        process_country(
            country
        )


    print("\n")
    print(
        "ALL COUNTRIES RISK CALCULATION COMPLETED"
    )