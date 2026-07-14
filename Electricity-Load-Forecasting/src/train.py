from pathlib import Path
import joblib
import json

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent


FEATURES = [
    "temperature",
    "wind_speed",
    "cloud_cover",
    "solar_radiation",
    "hour",
    "month",
    "weekday",
    "weekend",
    "load_lag_1",
    "load_lag_24",
    "load_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "hour_sin",
    "hour_cos"
]


def train_xgboost(
    df,
    country="Germany"
):
    """
    Train XGBoost model for selected country.
    """


    model_dir = (
        BASE_DIR
        / "models"
        / country
    )


    model_dir.mkdir(
        exist_ok=True
    )


    X = df[FEATURES]

    y = df["load"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )


    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )


    model.fit(
        X_train,
        y_train
    )


    model_path = (
        model_dir
        / "xgboost_load_forecasting.pkl"
    )


    joblib.dump(
        model,
        model_path
    )


    features_path = (
        model_dir
        / "features.json"
    )


    with open(
        features_path,
        "w"
    ) as f:

        json.dump(
            FEATURES,
            f,
            indent=4
        )


    return model