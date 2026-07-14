from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


COUNTRY_LOAD_COLUMNS = {

    "Germany":
        "DE_load_actual_entsoe_transparency",

    "France":
        "FR_load_actual_entsoe_transparency",

    "Spain":
        "ES_load_actual_entsoe_transparency",

    "Netherlands":
        "NL_load_actual_entsoe_transparency"
}



def load_country_energy(country="Germany"):

    file_path = (
        BASE_DIR
        / "data"
        / "raw"
        / "time_series.csv"
    )


    df = pd.read_csv(
    file_path,
    parse_dates=["utc_timestamp"]
)


    df["utc_timestamp"] = (
    df["utc_timestamp"]
    .dt.tz_localize(None)
)


    column = COUNTRY_LOAD_COLUMNS[country]


    energy = df[
        [
            "utc_timestamp",
            column
        ]
    ].copy()


    energy = energy.rename(
        columns={
            "utc_timestamp": "datetime",
            column: "load"
        }
    )


    energy = energy.dropna()


    return energy