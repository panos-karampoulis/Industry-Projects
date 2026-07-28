import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


INPUT_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_prices.csv"
)


OUTPUT_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_features.csv"
)



# ============================================================
# TIMEZONE CONFIG
# ============================================================

TIMEZONES = {

    "germany": "Europe/Berlin",
    "france": "Europe/Paris",
    "spain": "Europe/Madrid",
    "italy": "Europe/Rome",
    "netherlands": "Europe/Amsterdam"

}



# ============================================================
# LOAD DATA
# ============================================================

print("="*60)
print("Loading dataset")
print("="*60)


df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["timestamp"]
)


df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    utc=True
)


print(df.head())

print(
    "Original shape:",
    df.shape
)



# ============================================================
# KEEP ONLY PT15M
# ============================================================

df = df[
    df["resolution"] == "PT15M"
].copy()



print(
    "After PT15M filter:",
    df.shape
)



# ============================================================
# TIME FEATURES FUNCTION
# ============================================================


def add_time_features(group):


    country = group["country"].iloc[0]


    timezone = TIMEZONES[country]


    # UTC -> local timezone

    local_time = (
        group["timestamp"]
        .dt
        .tz_convert(timezone)
    )


    group["local_timestamp"] = local_time



    # DST flag

    group["dst_flag"] = (

        local_time
        .map(
            lambda x:
            int(
                x.dst() != pd.Timedelta(0)
            )
        )

    )



    group["hour"] = (
        local_time.dt.hour
    )


    group["day_of_week"] = (
        local_time.dt.dayofweek
    )


    group["month"] = (
        local_time.dt.month
    )


    group["year"] = (
        local_time.dt.year
    )


    group["weekend"] = (

        local_time.dt.dayofweek >= 5

    ).astype(int)



    # --------------------------------------------------------
    # Season
    # --------------------------------------------------------

    def season(month):

        if month in [12,1,2]:
            return "winter"

        elif month in [3,4,5]:
            return "spring"

        elif month in [6,7,8]:
            return "summer"

        else:
            return "autumn"



    group["season"] = (
        group["month"]
        .apply(season)
    )



    # --------------------------------------------------------
    # Peak / Off Peak
    # --------------------------------------------------------


    group["is_peak"] = (

        (group["hour"] >= 8)

        &

        (group["hour"] < 20)

        &

        (group["weekend"] == 0)

    ).astype(int)



    group["is_off_peak"] = (

        group["is_peak"] == 0

    ).astype(int)



    # --------------------------------------------------------
    # Intraday periods
    # --------------------------------------------------------


    group["night_period"] = (

        (group["hour"] >= 0)

        &

        (group["hour"] < 7)

    ).astype(int)



    group["morning_ramp"] = (

        (group["hour"] >= 7)

        &

        (group["hour"] < 10)

    ).astype(int)



    group["evening_peak"] = (

        (group["hour"] >= 17)

        &

        (group["hour"] < 21)

    ).astype(int)



    return group




# ============================================================
# APPLY TIME FEATURES
# ============================================================


print("Creating time features...")


countries = []


for country, group in df.groupby("country"):


    group = group.sort_values(
        "timestamp"
    )


    group = add_time_features(
        group
    )


    countries.append(
        group
    )



df = pd.concat(
    countries,
    ignore_index=True
)



# ============================================================
# LAG FEATURES
# ============================================================


print("Creating lag features...")



df = df.sort_values(
    [
        "country",
        "timestamp"
    ]
)



# previous 15 minutes

df["lag_1"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(1)

)



# previous hour

df["lag_4"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(4)

)



# previous day

df["lag_96"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(96)

)



# previous week

df["lag_672"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(672)

)




# ============================================================
# ROLLING FEATURES
# ============================================================


print("Creating rolling features...")



df["rolling_mean_96"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(1)
    .rolling(96)
    .mean()

)



df["rolling_std_96"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(1)
    .rolling(96)
    .std()

)



df["rolling_mean_672"] = (

    df
    .groupby("country")
    ["price_eur_mwh"]
    .shift(1)
    .rolling(672)
    .mean()

)



# ============================================================
# CLEAN
# ============================================================


df = df.dropna()


df = df.reset_index(
    drop=True
)



# ============================================================
# SAVE
# ============================================================


OUTPUT_FILE.parent.mkdir(
    exist_ok=True,
    parents=True
)



df.to_csv(
    OUTPUT_FILE,
    index=False
)



# ============================================================
# RESULTS
# ============================================================


print("="*60)
print("FEATURE ENGINEERING COMPLETED")
print("="*60)


print(
    df.head()
)


print(
    "Final shape:",
    df.shape
)


print(
    "Columns:"
)

print(
    df.columns.tolist()
)


print(
    "Saved:",
    OUTPUT_FILE
)