import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)







import warnings

warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np


from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


from sklearn.preprocessing import StandardScaler


from sklearn.linear_model import LinearRegression


from sklearn.ensemble import RandomForestRegressor


from xgboost import XGBRegressor


import joblib



# Prophet optional
try:

    from prophet import Prophet

    PROPHET_AVAILABLE = True

except:

    PROPHET_AVAILABLE = False



from src.config.countries import (
    get_active_countries
)




# ============================================================
# PATHS
# ============================================================


BASE_DIR = Path(__file__).resolve().parents[2]


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


MODEL_DIR = (
    BASE_DIR
    /
    "models"
    /
    "load_forecasting"
)


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# ============================================================
# METRICS
# ============================================================


def evaluate_model(
        y_true,
        y_pred
):


    mae = mean_absolute_error(
        y_true,
        y_pred
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )


    return mae, rmse




# ============================================================
# LOAD DATA
# ============================================================


def load_country_data(
        country
):


    path = (
        PROCESSED_DIR
        /
        f"{country}_load_features.csv"
    )


    if not path.exists():

        raise FileNotFoundError(
            f"Missing data: {path}"
        )


    df = pd.read_csv(
        path
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )


    df = df.sort_values(
        "timestamp"
    )


    return df




# ============================================================
# FEATURE PREPARATION
# ============================================================


def prepare_data(
        df
):


    target = "load_mw"


    drop_columns = [

        "timestamp",
        "country",
        target

    ]


    X = df.drop(
        columns=[
            c for c in drop_columns
            if c in df.columns
        ]
    )


    y = df[target]



    # remove missing

    data = pd.concat(
        [
            X,
            y
        ],
        axis=1
    ).dropna()



    X = data.drop(
        columns=[
            target
        ]
    )


    y = data[target]



    return X, y




# ============================================================
# PROPHET
# ============================================================


def train_prophet(
        df,
        country
):


    if not PROPHET_AVAILABLE:

        print(
            "Prophet not installed - skipping"
        )

        return None



    print(
        "Training Prophet..."
    )


    prophet_df = df[
        [
            "timestamp",
            "load_mw"
        ]
    ].rename(
        columns={
            "timestamp": "ds",
            "load_mw": "y"
        }
    )


    # Prophet does not support timezone timestamps
    prophet_df["ds"] = (
        pd.to_datetime(
            prophet_df["ds"]
        )
        .dt.tz_localize(None)
    )



    model = Prophet(

        yearly_seasonality=True,

        weekly_seasonality=True,

        daily_seasonality=True

    )



    model.fit(
        prophet_df
    )



    folder = (
        MODEL_DIR
        /
        country
    )


    folder.mkdir(
        exist_ok=True
    )


    joblib.dump(

        model,

        folder
        /
        "prophet.pkl"

    )


    print(
        "Prophet saved"
    )


    return model




# ============================================================
# MAIN TRAINING
# ============================================================


def train_country(
        country
):


    print("\n")
    print("="*70)

    print(
        f"TRAINING: {country.upper()}"
    )

    print("="*70)



    df = load_country_data(
        country
    )



    X, y = prepare_data(
        df
    )



    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        shuffle=False

    )



    results = []



    folder = (
        MODEL_DIR
        /
        country
    )


    folder.mkdir(
        exist_ok=True
    )



    # =====================================================
    # LINEAR REGRESSION
    # =====================================================


    print(
        "Training Linear Regression"
    )


    lr = LinearRegression()


    lr.fit(
        X_train,
        y_train
    )


    pred = lr.predict(
        X_test
    )


    mae, rmse = evaluate_model(

        y_test,
        pred

    )


    results.append(

        [
            "Linear Regression",
            mae,
            rmse
        ]

    )


    joblib.dump(

        lr,

        folder
        /
        "linear_regression.pkl"

    )



    # =====================================================
    # RANDOM FOREST
    # =====================================================


    print(
        "Training Random Forest"
    )


    rf = RandomForestRegressor(

        n_estimators=100,

        random_state=42,

        n_jobs=-1

    )


    rf.fit(

        X_train,

        y_train

    )


    pred = rf.predict(
        X_test
    )


    mae, rmse = evaluate_model(

        y_test,

        pred

    )


    results.append(

        [
            "Random Forest",
            mae,
            rmse
        ]

    )



    joblib.dump(

        rf,

        folder
        /
        "random_forest.pkl"

    )



    # =====================================================
    # XGBOOST
    # =====================================================


    print(
        "Training XGBoost"
    )


    xgb = XGBRegressor(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42

    )



    xgb.fit(

        X_train,

        y_train

    )



    pred = xgb.predict(

        X_test

    )


    mae, rmse = evaluate_model(

        y_test,

        pred

    )


    results.append(

        [
            "XGBoost",
            mae,
            rmse
        ]

    )



    joblib.dump(

        xgb,

        folder
        /
        "xgboost.pkl"

    )



    # =====================================================
    # PROPHET
    # =====================================================


    train_prophet(

        df,

        country

    )



    results_df = pd.DataFrame(

        results,

        columns=[

            "model",
            "MAE",
            "RMSE"

        ]

    )


    print()

    print(
        results_df
    )


    results_df.to_csv(

        folder
        /
        "metrics.csv",

        index=False

    )


    print()

    print(
        "MODELS SAVED"
    )





# ============================================================
# RUN ALL COUNTRIES
# ============================================================


def main():


    countries = get_active_countries()



    for country in countries:


        try:

            train_country(
                country
            )


        except Exception as e:


            print()

            print(
                f"FAILED {country}"
            )

            print(
                repr(e)
            )




    print()

    print("="*70)

    print(
        "LOAD FORECASTING COMPLETED"
    )

    print("="*70)




if __name__ == "__main__":

    main()