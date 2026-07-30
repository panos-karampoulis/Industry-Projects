import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os



# ============================================================
# PATHS
# ============================================================

DATA_FILE = (
    "data/features/germany_features.csv"
)


RF_MODEL = (
    "models/random_forest_model.pkl"
)


XGB_MODEL = (
    "models/xgboost_model.pkl"
)


OUTPUT_DIR = (
    "results/plots"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



# ============================================================
# LOAD DATA
# ============================================================


print("="*70)
print("FORECAST VISUALIZATION")
print("="*70)



df = pd.read_csv(
    DATA_FILE,
    index_col=0,
    parse_dates=True
)


df = df.sort_index()



# ============================================================
# TRAIN TEST SPLIT
# ============================================================


split = int(
    len(df)*0.8
)


test = df.iloc[split:]



print("\nTest dataset:")
print(test.shape)



# ============================================================
# FEATURES
# ============================================================


target = "price_eur_mwh"


features = [

    "load_mw",

    "biomass_mw",
    "lignite_mw",
    "gas_mw",
    "hard_coal_mw",

    "hydro_run_mw",
    "hydro_reservoir_mw",

    "solar_mw",

    "wind_offshore_mw",
    "wind_onshore_mw",

    "renewable_generation",
    "renewable_share",
    "residual_load",

    "hour",
    "day_of_week",
    "day_of_year",
    "month",
    "quarter",
    "weekend",

    "price_lag_1",
    "price_lag_24",
    "price_lag_48",
    "price_lag_168",

    "price_mean_24h",
    "price_std_24h",

    "price_mean_168h",
    "price_std_168h"

]



X_test = test[features]

y_test = test[target]



# ============================================================
# LOAD MODELS
# ============================================================


print("\nLoading models...")


rf_model = joblib.load(
    RF_MODEL
)


xgb_model = joblib.load(
    XGB_MODEL
)



print("Models loaded")



# ============================================================
# PREDICTIONS
# ============================================================


print("\nCreating forecasts...")


rf_prediction = rf_model.predict(
    X_test
)


xgb_prediction = xgb_model.predict(
    X_test
)



# ============================================================
# CREATE FORECAST DATAFRAME
# ============================================================


forecast_df = pd.DataFrame({

    "actual": y_test,

    "random_forest": rf_prediction,

    "xgboost": xgb_prediction

}, index=y_test.index)



forecast_df.to_csv(
    "results/forecast_predictions.csv"
)



print("\nSaved:")
print(
    "results/forecast_predictions.csv"
)



# ============================================================
# RANDOM FOREST PLOT
# ============================================================


plt.figure(
    figsize=(14,6)
)


plt.plot(
    forecast_df.index,
    forecast_df["actual"],
    label="Actual"
)


plt.plot(
    forecast_df.index,
    forecast_df["random_forest"],
    label="Random Forest"
)


plt.title(
    "Day Ahead Price Forecast - Random Forest"
)


plt.ylabel(
    "Price €/MWh"
)


plt.legend()

plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    f"{OUTPUT_DIR}/rf_forecast_vs_actual.png",
    dpi=300
)


plt.close()



# ============================================================
# XGBOOST PLOT
# ============================================================


plt.figure(
    figsize=(14,6)
)


plt.plot(
    forecast_df.index,
    forecast_df["actual"],
    label="Actual"
)


plt.plot(
    forecast_df.index,
    forecast_df["xgboost"],
    label="XGBoost"
)


plt.title(
    "Day Ahead Price Forecast - XGBoost"
)


plt.ylabel(
    "Price €/MWh"
)


plt.legend()

plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    f"{OUTPUT_DIR}/xgb_forecast_vs_actual.png",
    dpi=300
)


plt.close()



# ============================================================
# ONE WEEK ZOOM
# ============================================================


week = forecast_df.iloc[-168:]



plt.figure(
    figsize=(14,6)
)


plt.plot(
    week.index,
    week["actual"],
    label="Actual"
)


plt.plot(
    week.index,
    week["random_forest"],
    label="Random Forest"
)


plt.plot(
    week.index,
    week["xgboost"],
    label="XGBoost"
)


plt.title(
    "One Week Forecast Comparison"
)


plt.ylabel(
    "Price €/MWh"
)


plt.legend()

plt.grid(
    True
)


plt.tight_layout()


plt.savefig(
    f"{OUTPUT_DIR}/one_week_forecast_comparison.png",
    dpi=300
)


plt.close()



print("\nPlots created:")

print(
    "rf_forecast_vs_actual.png"
)

print(
    "xgb_forecast_vs_actual.png"
)

print(
    "one_week_forecast_comparison.png"
)


print("\nDONE")