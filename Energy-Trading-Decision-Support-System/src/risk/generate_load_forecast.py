import os
import sys
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# -----------------------------
# Country argument
# -----------------------------

if len(sys.argv) < 2:
    raise ValueError(
        "Usage: python generate_load_forecast.py <country>"
    )


COUNTRY = sys.argv[1].lower()


DATA_PATH = (
    f"data/features/{COUNTRY}_features.csv"
)


MODEL_DIR = (
    f"models/{COUNTRY}"
)


MODEL_PATH = (
    f"{MODEL_DIR}/{COUNTRY}_load_forecaster.pkl"
)


FEATURE_PATH = (
    f"{MODEL_DIR}/{COUNTRY}_load_features.pkl"
)
# -----------------------------
# Load Dataset
# -----------------------------

def load_data():

    df = pd.read_csv(DATA_PATH)

    # timestamp column
    df["timestamp"] = df["Unnamed: 0"]

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df = df.sort_values(
        "timestamp"
    )

    return df



# -----------------------------
# Prepare Features
# -----------------------------

def prepare_features(df):


    X = df.drop(
        columns=[
            "load_mw",
            "Unnamed: 0",
            "timestamp"
        ]
    )


    y = df["load_mw"]


    # Encode categorical variables

    categorical_cols = X.select_dtypes(
        include=["object", "string"]
    ).columns


    print(
        "Categorical columns:",
        categorical_cols.tolist()
    )


    X = pd.get_dummies(
        X,
        columns=categorical_cols,
        drop_first=True
    )

    # -----------------------------
    # Handle infinite values
    # -----------------------------

    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )


    # -----------------------------
    # Fill missing values
    # -----------------------------

    X = X.ffill()

    X = X.fillna(0)

    return X, y


# -----------------------------
# Train Models
# -----------------------------

def train_models(X, y):


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )


    models = {

        "Random Forest":
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            ),


        "XGBoost":
            XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )

    }


    results = {}


    best_model = None
    best_rmse = float("inf")


    for name, model in models.items():

        print(
            f"\nTraining {name}..."
        )

        model.fit(
            X_train,
            y_train
        )


        predictions = model.predict(
            X_test
        )


        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = mean_squared_error(
            y_test,
            predictions
        ) ** 0.5


        print(
            f"{name}"
        )

        print(
            f"MAE: {mae:.2f} MW"
        )

        print(
            f"RMSE: {rmse:.2f} MW"
        )


        results[name] = rmse


        if rmse < best_rmse:

            best_rmse = rmse
            best_model = model



    print(
        "\nBest model RMSE:",
        best_rmse
    )


    return best_model



# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":


    print(
        "Loading data..."
    )


    df = load_data()


    print(
        "Dataset:",
        df.shape
    )


    X, y = prepare_features(
        df
    )


    model = train_models(
        X,
        y
    )


    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )


    joblib.dump(
        model,
        MODEL_PATH
    )


    joblib.dump(
        X.columns.tolist(),
        FEATURE_PATH
    )


    print(
        "Features saved:"
    )

    print(FEATURE_PATH)


    print(
        "\nModel saved:"
    )

    print(
        MODEL_PATH
    )