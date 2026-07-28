import pandas as pd
import os


# ============================================================
# Paths
# ============================================================

INPUT_PATH = (
    "data/final/germany/2020/"
    "germany_2020_full_dataset.csv"
)


OUTPUT_PATH = (
    "data/final/germany/2020/"
    "germany_2020_model_dataset.csv"
)



# ============================================================
# Feature creation
# ============================================================

def create_features(df):

    print("="*60)
    print("Creating forecasting features")
    print("="*60)


    # -----------------------------
    # Price lags
    # -----------------------------

    print("Creating price lags...")


    df["price_lag_1"] = (
        df["price_eur_mwh"]
        .shift(1)
    )


    df["price_lag_24"] = (
        df["price_eur_mwh"]
        .shift(24)
    )


    df["price_lag_48"] = (
        df["price_eur_mwh"]
        .shift(48)
    )


    df["price_lag_168"] = (
        df["price_eur_mwh"]
        .shift(168)
    )



    # -----------------------------
    # Rolling statistics
    # -----------------------------

    print("Creating rolling statistics...")


    df["price_rolling_mean_24"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .mean()
    )


    df["price_rolling_std_24"] = (
        df["price_eur_mwh"]
        .rolling(24)
        .std()
    )



    # -----------------------------
    # Energy lags
    # -----------------------------

    print("Creating energy lags...")


    df["load_lag_24"] = (
        df["load_mw"]
        .shift(24)
    )


    df["renewable_lag_24"] = (
        df["renewable_generation"]
        .shift(24)
    )


    df["residual_load_lag_24"] = (
        df["residual_load"]
        .shift(24)
    )



    # -----------------------------
    # Target
    # -----------------------------

    print("Creating forecasting target...")


    df["target_price_24h"] = (
        df["price_eur_mwh"]
        .shift(-24)
    )



    return df



# ============================================================
# Main
# ============================================================

def main():

    print("Loading dataset...")

    df = pd.read_csv(
        INPUT_PATH,
        index_col="datetime",
        parse_dates=True
    )


    print("\nOriginal:")
    print(df.shape)



    df = create_features(df)



    # remove rows with missing lag values

    df = df.dropna()



    print("\nAfter feature engineering:")
    print(df.shape)



    print("\nColumns:")
    print(df.columns.tolist())



    print("\nSaving...")


    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_PATH
    )



    print("\nSaved:")
    print(OUTPUT_PATH)



if __name__ == "__main__":
    main()