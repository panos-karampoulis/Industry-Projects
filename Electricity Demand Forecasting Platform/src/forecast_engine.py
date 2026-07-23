import pandas as pd
import numpy as np
import joblib

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent



def generate_forecast(
        country,
        forecast_date=None
):


    country = country.lower()



    # -----------------------------------
    # Paths
    # -----------------------------------

    dataset_file = (

        BASE_DIR
        /
        "data"
        /
        "processed"
        /
        country
        /
        "load_weather_dataset.csv"

    )


    model_file = (

        BASE_DIR
        /
        "models"
        /
        country
        /
        "xgboost_load_forecaster_v3.pkl"

    )



    if not dataset_file.exists():

        raise FileNotFoundError(
            f"No dataset found for {country}"
        )


    if not model_file.exists():

        raise FileNotFoundError(
            f"No model found for {country}"
        )



    # -----------------------------------
    # Load data
    # -----------------------------------

    df = pd.read_csv(

        dataset_file,

        parse_dates=[
            "datetime"
        ]

    )


    df = (

        df
        .sort_values("datetime")
        .reset_index(drop=True)

    )



    # -----------------------------------
    # Features
    # -----------------------------------

    df["hour"] = (
        df.datetime.dt.hour
    )


    df["day_of_week"] = (
        df.datetime.dt.dayofweek
    )


    df["month"] = (
        df.datetime.dt.month
    )


    df["day_of_year"] = (
        df.datetime.dt.dayofyear
    )


    df["week_of_year"] = (

        df.datetime
        .dt.isocalendar()
        .week
        .astype(int)

    )


    df["is_weekend"] = (

        df.day_of_week >= 5

    ).astype(int)



    # cyclic

    df["hour_sin"] = (

        np.sin(
            2*np.pi*df.hour/24
        )

    )


    df["hour_cos"] = (

        np.cos(
            2*np.pi*df.hour/24
        )

    )


    df["day_year_sin"] = (

        np.sin(
            2*np.pi*df.day_of_year/365
        )

    )


    df["day_year_cos"] = (

        np.cos(
            2*np.pi*df.day_of_year/365
        )

    )



    # demand history


    df["load_lag_24"] = (

        df.load_mwh
        .shift(24)

    )


    df["load_lag_168"] = (

        df.load_mwh
        .shift(168)

    )


    df["load_lag_8760"] = (

        df.load_mwh
        .shift(8760)

    )


    df["load_mean_24"] = (

        df.load_mwh
        .shift(1)
        .rolling(24)
        .mean()

    )


    df["load_mean_168"] = (

        df.load_mwh
        .shift(1)
        .rolling(168)
        .mean()

    )


    df["load_mean_720"] = (

        df.load_mwh
        .shift(1)
        .rolling(720)
        .mean()

    )


    df["load_std_24"] = (

        df.load_mwh
        .shift(1)
        .rolling(24)
        .std()

    )



    df = df.dropna()



    # -----------------------------------
    # Forecast date
    # -----------------------------------

    if forecast_date is None:

        forecast_date = (

            pd.Timestamp.today()
            +
            pd.Timedelta(days=1)

        ).date()

    else:

        forecast_date = pd.to_datetime(
            forecast_date
        ).date()



    # -----------------------------------
    # Select latest weather day
    # -----------------------------------

    forecast_day = df[

        df.datetime.dt.date
        ==
        forecast_date

    ]


    # If future date is not inside historical data
    # use the last available 24 weather hours

    if len(forecast_day) == 0:

        forecast_day = (

            df
            .tail(24)
            .copy()

        )


        forecast_day["datetime"] = (

            pd.date_range(

                start=pd.to_datetime(forecast_date),

                periods=24,

                freq="h"

            )

        )


    # -----------------------------------
    # Features
    # -----------------------------------

    features = [

        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "cloud_cover",
        "surface_pressure",
        "shortwave_radiation",

        "hour",
        "day_of_week",
        "month",
        "day_of_year",
        "week_of_year",
        "is_weekend",

        "hour_sin",
        "hour_cos",
        "day_year_sin",
        "day_year_cos",

        "load_lag_24",
        "load_lag_168",
        "load_lag_8760",

        "load_mean_24",
        "load_mean_168",
        "load_mean_720",

        "load_std_24"

    ]



    X = forecast_day[features]



    # ensure numeric

    X = X.astype(float)



    # -----------------------------------
    # Load model
    # -----------------------------------

    model = joblib.load(
        model_file
    )



    # -----------------------------------
    # Predict
    # -----------------------------------

    prediction = model.predict(
        X
    )



    result = pd.DataFrame({

    "datetime":
    forecast_day.datetime,

    "forecast_load_mw":
    prediction

})


    # -----------------------------------
    # Forecast KPIs
    # -----------------------------------

    average_load = (

        result["forecast_load_mw"]
        .mean()

    )


    peak_load = (

        result["forecast_load_mw"]
        .max()

    )


    peak_index = (

        result["forecast_load_mw"]
        .idxmax()

    )


    peak_hour = (

        result
        .loc[peak_index, "datetime"]

    )


    daily_energy_gwh = (

        result["forecast_load_mw"]
        .sum()
        /
        1000

    )



    summary = {

        "average_load_mw":
        round(
            average_load,
            2
        ),


        "peak_load_mw":
        round(
            peak_load,
            2
        ),


        "peak_hour":
        peak_hour.strftime(
            "%H:%M"
        ),


        "daily_energy_gwh":
        round(
            daily_energy_gwh,
            2
        )

    }

    # -----------------------------------
    # Save forecast report
    # -----------------------------------

    report_dir = (

        BASE_DIR
        /
        "reports"
        /
        "forecasts"
        /
        country

    )


    report_dir.mkdir(

        parents=True,

        exist_ok=True

    )



    forecast_file = (

        report_dir
        /
        f"{country}_forecast_{forecast_date}.csv"

    )



    result.to_csv(

        forecast_file,

        index=False

    )

    return result, summary