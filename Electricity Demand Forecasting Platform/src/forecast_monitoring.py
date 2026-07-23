import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent



def calculate_forecast_accuracy(
    country,
    forecast_file,
    actual_file
):


    # -------------------------
    # Load data
    # -------------------------

    forecast = pd.read_csv(
        forecast_file,
        parse_dates=["datetime"]
    )


    actual = pd.read_csv(
        actual_file,
        parse_dates=["datetime"]
    )


    # -------------------------
    # Rename columns
    # -------------------------

    forecast = forecast.rename(
        columns={
            "forecast_load_mw":
            "forecast_mw"
        }
    )


    actual = actual.rename(
        columns={
            "load_mwh":
            "actual_mw"
        }
    )


    # -------------------------
    # Merge
    # -------------------------

    df = pd.merge(

        forecast,

        actual,

        on="datetime",

        how="inner"

    )


    # -------------------------
    # Errors
    # -------------------------

    df["error_mw"] = (

        df["actual_mw"]

        -

        df["forecast_mw"]

    )


    df["absolute_error_mw"] = (

        df["error_mw"]
        .abs()

    )


    df["percentage_error"] = (

        df["absolute_error_mw"]

        /

        df["actual_mw"]

        *

        100

    )


    # -------------------------
    # Metrics
    # -------------------------

    results = {


        "country": country,


        "MAE_MW":

            df["absolute_error_mw"]
            .mean(),


        "MAPE_%":

            df["percentage_error"]
            .mean(),


        "Bias_MW":

            df["error_mw"]
            .mean()


    }



    # -------------------------
    # Save
    # -------------------------

    output_dir = (

        BASE_DIR

        /

        "reports"

        /

        "monitoring"

    )


    output_dir.mkdir(

        parents=True,

        exist_ok=True

    )


    output_file = (

        output_dir

        /

        "forecast_accuracy.csv"

    )


    result_df = pd.DataFrame(
        [results]
    )


    if output_file.exists():

        old = pd.read_csv(
            output_file
        )

        result_df = pd.concat(
            [
                old,
                result_df
            ],
            ignore_index=True
        )


    result_df.to_csv(

        output_file,

        index=False

    )


    print(
        result_df
    )


    print()

    print(
        f"Saved:\n{output_file}"
    )



if __name__ == "__main__":


    print(
        "Forecast Monitoring Module"
    )