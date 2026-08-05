import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

INPUT_DIR = r"D:\Portfolio\Energy-Trading-Decision-Support-System\data\features"

OUTPUT_DIR = r"D:\Portfolio\Energy-Trading-Decision-Support-System\data\features\final"


os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    "germany",
    "france",
    "netherlands",
    "spain",
    "italy"
]


# ============================================================
# CLEAN RISK FEATURES
# ============================================================

for country in COUNTRIES:

    print("\n" + "="*70)
    print(f"PROCESSING {country.upper()}")
    print("="*70)


    input_file = os.path.join(
        INPUT_DIR,
        f"{country}_features_with_risk.csv"
    )


    output_file = os.path.join(
        OUTPUT_DIR,
        f"{country}_features_risk_final.csv"
    )


    if not os.path.exists(input_file):

        print("Missing file:")
        print(input_file)
        continue


    # Load data

    df = pd.read_csv(
        input_file,
        index_col=0,
        parse_dates=True
    )


    print("Original shape:")
    print(df.shape)


    print("Missing values before:")
    print(df.isna().sum().sum())


    # ========================================================
    # CLEANING
    # ========================================================


    # Forward fill time-series values
    df = df.ffill()


    # Back fill remaining initial values
    df = df.bfill()


    # Replace infinite values

    df.replace(
        [float("inf"), float("-inf")],
        pd.NA,
        inplace=True
    )


    # Final fill

    df = df.fillna(0)


    # ========================================================
    # SAVE
    # ========================================================

    df.to_csv(output_file)


    print("Missing values after:")
    print(df.isna().sum().sum())


    print("Final shape:")
    print(df.shape)


    print("Saved:")
    print(output_file)


print("\n")
print("="*70)
print("RISK FEATURE CLEANUP COMPLETED")
print("="*70)