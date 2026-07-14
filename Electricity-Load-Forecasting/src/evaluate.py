from pathlib import Path
import json

import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)


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


def evaluate_model(
    model,
    df,
    country="Germany"
):
    """
    Evaluate forecasting model for selected country.
    """


    X = df[FEATURES]

    y = df["load"]


    predictions = model.predict(
        X
    )


    mae = mean_absolute_error(
        y,
        predictions
    )


    rmse = np.sqrt(
        mean_squared_error(
            y,
            predictions
        )
    )


    mape = mean_absolute_percentage_error(
        y,
        predictions
    )


    results = {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "MAPE": float(mape)
    }


    results_dir = (
        BASE_DIR
        / "results"
        / country
    )


    results_dir.mkdir(
        exist_ok=True
    )


    results_path = (
        results_dir
        / "metrics.json"
    )


    with open(
        results_path,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )


    return results