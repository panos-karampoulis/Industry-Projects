import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"


# ---------------------------------------
# Forecast date
# ---------------------------------------

forecast_date = "2026-07-24"


forecast_date = pd.to_datetime(
    forecast_date
)



# ---------------------------------------
# Create future hourly timestamps
# ---------------------------------------

future_dates = pd.date_range(
    start=forecast_date,
    periods=24,
    freq="h"
)


future = pd.DataFrame({

    "datetime": future_dates

})



# ---------------------------------------
# Calendar features
# ---------------------------------------

future["hour"] = (
    future["datetime"]
    .dt.hour
)


future["day_of_week"] = (
    future["datetime"]
    .dt.dayofweek
)


future["month"] = (
    future["datetime"]
    .dt.month
)


future["is_weekend"] = (
    future["day_of_week"] >= 5
).astype(int)



# ---------------------------------------
# Save temporary future features
# ---------------------------------------

output_dir = (
    BASE_DIR
    /
    "data"
    /
    "future"
    /
    country
)


output_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_file = (
    output_dir
    /
    f"future_features_{forecast_date.date()}.csv"
)


future.to_csv(
    output_file,
    index=False
)



print(
    future
)


print()

print(
    f"Saved:\n{output_file}"
)