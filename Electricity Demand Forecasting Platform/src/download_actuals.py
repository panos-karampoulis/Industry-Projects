import argparse
from pathlib import Path

import pandas as pd
import yaml

from entsoe_client import get_client
from time_utils import convert_to_utc
from entsoe.exceptions import NoMatchingDataError


BASE_DIR = Path(__file__).resolve().parent.parent



CONFIG_FILE = (

    BASE_DIR
    /
    "configs"
    /
    "countries.yaml"

)



with open(CONFIG_FILE, "r") as f:

    COUNTRIES = yaml.safe_load(f)



# ---------------------------------------
# Arguments
# ---------------------------------------

parser = argparse.ArgumentParser()


parser.add_argument(

    "--country",

    required=True

)


parser.add_argument(

    "--date",

    required=True,

    help="YYYY-MM-DD"

)


args = parser.parse_args()



country = args.country.lower()

date = args.date



if country not in COUNTRIES:

    raise ValueError(
        f"{country} not found"
    )



country_code = COUNTRIES[country]["entsoe_code"]

timezone = COUNTRIES[country]["timezone"]



# ---------------------------------------
# ENTSO-E
# ---------------------------------------

client = get_client()



start = pd.Timestamp(

    date,

    tz=timezone

)


end = start + pd.Timedelta(

    days=1

)



print()

print(
    f"Downloading actual load for {country}"
)

print(
    start,
    end
)



try:

    load = client.query_load(
        country_code=country_code,
        start=start,
        end=end
    )

except NoMatchingDataError:

    print()

    print("=" * 40)
    print("Actual data not available")
    print("=" * 40)

    print()

    print(
        "ENTSO-E has not yet published\n"
        f"actual demand for {date}."
    )

    print()

    print("Monitoring skipped.")

    exit()



# ---------------------------------------
# Dataframe
# ---------------------------------------

load = load.reset_index()



load.columns = [

    "datetime",

    "load_mwh"

]



# Convert 15 min → hourly

load = (

    load

    .set_index("datetime")

    .resample("1h")

    .mean()

    .dropna()

    .reset_index()

)



load = convert_to_utc(

    load,

    timezone=timezone

)



# ---------------------------------------
# Save
# ---------------------------------------

output_dir = (

    BASE_DIR

    /

    "reports"

    /

    "actuals"

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

    f"{country}_actual_{date}.csv"

)



load.to_csv(

    output_file,

    index=False

)



print()

print(load.head())

print()

print(
    f"Saved:\n{output_file}"
)