import pandas as pd
import os


# ============================================================
# PATHS
# ============================================================

INPUT_FILE = (
    "data/processed/germany/germany_clean.csv"
)


OUTPUT_FILE = (
    "data/features/germany_features.csv"
)



# ============================================================
# LOAD DATA
# ============================================================

print("="*70)
print("CREATING FEATURES")
print("="*70)


df = pd.read_csv(
    INPUT_FILE,
    index_col=0,
    parse_dates=True
)


print("\nOriginal dataset:")
print(df.shape)



# ============================================================
# TIME FEATURES
# ============================================================

print("\nCreating time features...")


df["hour"] = (
    df.index.hour
)


df["day_of_week"] = (
    df.index.dayofweek
)


df["day_of_year"] = (
    df.index.dayofyear
)


df["month"] = (
    df.index.month
)


df["quarter"] = (
    df.index.quarter
)


df["weekend"] = (
    df["day_of_week"]
    .isin([5,6])
    .astype(int)
)



# ============================================================
# PRICE LAGS
# ============================================================

print("Creating price lags...")


df["price_lag_1"] = (
    df["price_eur_mwh"]
    .shift(1)
)


df["price_lag_24"] = (
    df["price_eur_mwh"]
    .shift(24)
)


df["price_lag_48"] = (
    df["price_eur_mwh"]
    .shift(48)
)


df["price_lag_168"] = (
    df["price_eur_mwh"]
    .shift(168)
)



# ============================================================
# ROLLING FEATURES
# ============================================================

print("Creating rolling statistics...")


df["price_mean_24h"] = (
    df["price_eur_mwh"]
    .rolling(24)
    .mean()
)


df["price_std_24h"] = (
    df["price_eur_mwh"]
    .rolling(24)
    .std()
)


df["price_mean_168h"] = (
    df["price_eur_mwh"]
    .rolling(168)
    .mean()
)


df["price_std_168h"] = (
    df["price_eur_mwh"]
    .rolling(168)
    .std()
)



# ============================================================
# ENERGY FEATURES
# ============================================================

print("Creating energy features...")


renewables = [

    "solar_mw",
    "wind_onshore_mw",
    "wind_offshore_mw",
    "hydro_run_mw",
    "hydro_reservoir_mw",
    "biomass_mw"

]


df["renewable_generation"] = (
    df[renewables]
    .sum(axis=1)
)



df["renewable_share"] = (

    df["renewable_generation"]

    /

    df["load_mw"]

)



# ============================================================
# RESIDUAL LOAD
# ============================================================


df["residual_load"] = (

    df["load_mw"]

    -

    df["renewable_generation"]

)



# ============================================================
# CLEAN
# ============================================================

print("\nCleaning missing values...")


df = df.dropna()



df = df.sort_index()



# ============================================================
# CHECK
# ============================================================


print("\nFINAL FEATURES DATASET")

print(
    df.head()
)


print("\nShape:")
print(
    df.shape
)


print("\nDate range:")

print(
    df.index.min(),
    df.index.max()
)


print("\nMissing values:")

print(
    df.isna().sum().sum()
)



# ============================================================
# SAVE
# ============================================================


os.makedirs(
    "data/features",
    exist_ok=True
)


df.to_csv(
    OUTPUT_FILE
)


print("\nSaved:")
print(
    OUTPUT_FILE
)


print("\nDONE")