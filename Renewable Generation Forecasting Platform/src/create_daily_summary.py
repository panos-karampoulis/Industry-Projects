import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


COUNTRY = "germany"


FORECAST_FILE = (
    BASE_DIR
    /
    "reports"
    /
    COUNTRY
    /
    "renewable_forecast_results.csv"
)


OUTPUT_FILE = (
    BASE_DIR
    /
    "reports"
    /
    COUNTRY
    /
    "daily_summary.csv"
)



df = pd.read_csv(
    FORECAST_FILE,
    parse_dates=["datetime"]
)



daily = (
    df
    .groupby(
        df["datetime"].dt.date
    )
    .agg(
        renewable_total_mwh=(
            "renewable_total_mwh",
            "sum"
        ),

        prediction_mwh=(
            "prediction_mwh",
            "sum"
        ),

        absolute_error=(
            "absolute_error",
            "sum"
        )
    )
    .reset_index()
)



daily["error_mwh"] = (
    daily["renewable_total_mwh"]
    -
    daily["prediction_mwh"]
)



daily.rename(
    columns={
        "date": "datetime"
    },
    inplace=True
)



daily.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    "Daily summary created:"
)

print(
    OUTPUT_FILE
)