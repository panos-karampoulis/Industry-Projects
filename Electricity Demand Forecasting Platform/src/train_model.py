import pandas as pd
import numpy as np
import joblib
import json

from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor



BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"



# ---------------------------------------
# Load features
# ---------------------------------------

print("Loading features...")


file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    country
    /
    "load_features.csv"
)


df = pd.read_csv(
    file,
    parse_dates=["datetime"]
)


df = df.sort_values(
    "datetime"
)



# ---------------------------------------
# Train test split
# ---------------------------------------

print("Splitting dataset...")


train = df[
    df["datetime"] < "2025-01-01"
]


test = df[
    df["datetime"] >= "2025-01-01"
]



target = "target_load"


drop_columns = [
    "datetime",
    "target_load",
    "load_mwh"
]


features = [
    col for col in df.columns
    if col not in drop_columns
]



X_train = train[features]
y_train = train[target]


X_test = test[features]
y_test = test[target]



print()

print(
    "Train:",
    X_train.shape
)

print(
    "Test:",
    X_test.shape
)



# ---------------------------------------
# Models
# ---------------------------------------

models = {


    "Linear Regression":

    LinearRegression(),



    "Random Forest":

    RandomForestRegressor(

        n_estimators=200,

        random_state=42,

        n_jobs=-1

    ),



    "XGBoost":

    XGBRegressor(

        n_estimators=500,

        learning_rate=0.05,

        max_depth=6,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        n_jobs=-1

    )

}



results = []



best_model = None
best_rmse = float("inf")



# ---------------------------------------
# Training
# ---------------------------------------

for name, model in models.items():

    print()

    print(
        f"Training {name}..."
    )


    model.fit(
        X_train,
        y_train
    )


    prediction = model.predict(
        X_test
    )



    mae = mean_absolute_error(
        y_test,
        prediction
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            prediction
        )
    )


    mape = (
        np.abs(
            (y_test - prediction)
            /
            y_test
        )
    ).mean() * 100


    r2 = r2_score(
        y_test,
        prediction
    )


    print(
        f"MAE: {mae:.2f}"
    )

    print(
        f"RMSE: {rmse:.2f}"
    )

    print(
        f"MAPE: {mape:.2f}%"
    )

    print(
        f"R2: {r2:.4f}"
    )



    results.append({

        "model": name,

        "MAE": mae,

        "RMSE": rmse,

        "MAPE": mape,

        "R2": r2

    })



    if rmse < best_rmse:

        best_rmse = rmse

        best_model = model

        best_name = name



# ---------------------------------------
# Save metrics
# ---------------------------------------

report_dir = (
    BASE_DIR
    /
    "reports"
    /
    country
)


report_dir.mkdir(
    parents=True,
    exist_ok=True
)



metrics = pd.DataFrame(
    results
)


metrics.to_csv(
    report_dir /
    "model_metrics.csv",
    index=False
)



# ---------------------------------------
# Feature importance
# ---------------------------------------

if best_name == "XGBoost":

    importance = pd.DataFrame({

        "feature": features,

        "importance":
        best_model.feature_importances_

    })


    importance = (
        importance
        .sort_values(
            "importance",
            ascending=False
        )
    )


    importance.to_csv(
        report_dir /
        "feature_importance.csv",
        index=False
    )



# ---------------------------------------
# Save model
# ---------------------------------------

model_dir = (
    BASE_DIR
    /
    "models"
    /
    country
)


model_dir.mkdir(
    parents=True,
    exist_ok=True
)



joblib.dump(
    best_model,
    model_dir /
    "xgboost_load_forecaster.pkl"
)



metadata = {

    "country": country,

    "model": best_name,

    "training_period":
    "2020-01-01 to 2024-12-31",

    "test_period":
    "2025",

    "features":
    features,

    "MAE":
    float(
        metrics
        .loc[
            metrics["model"] == best_name,
            "MAE"
        ]
        .iloc[0]
    ),

    "RMSE":
    float(
        metrics
        .loc[
            metrics["model"] == best_name,
            "RMSE"
        ]
        .iloc[0]
    )

}



with open(
    model_dir /
    "metadata.json",
    "w"
) as f:

    json.dump(
        metadata,
        f,
        indent=4
    )



print()

print(
    "Best model:",
    best_name
)

print(
    "Training completed."
)