import pandas as pd
import matplotlib.pyplot as plt
import os



# ============================================================
# PATHS
# ============================================================

BASELINE_FILE = (
    "results/baseline_results.csv"
)

RF_FILE = (
    "results/random_forest_results.csv"
)

XGB_FILE = (
    "results/xgboost_results.csv"
)



OUTPUT_DIR = (
    "results/plots"
)



os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



# ============================================================
# LOAD RESULTS
# ============================================================


print("="*70)
print("MODEL COMPARISON")
print("="*70)



baseline = pd.read_csv(
    BASELINE_FILE
)


rf = pd.read_csv(
    RF_FILE
)


xgb = pd.read_csv(
    XGB_FILE
)



# combine

results = pd.concat(
    [
        baseline,
        rf,
        xgb
    ],
    ignore_index=True
)



print("\nMODEL RESULTS")

print(results)



# ============================================================
# SAVE COMBINED RESULTS
# ============================================================


results.to_csv(
    "results/model_comparison.csv",
    index=False
)



# ============================================================
# MAE COMPARISON
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(
    results["model"],
    results["MAE"]
)


plt.title(
    "Model Comparison - MAE"
)


plt.ylabel(
    "MAE (€/MWh)"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(
    f"{OUTPUT_DIR}/mae_comparison.png",
    dpi=300
)


plt.close()



# ============================================================
# RMSE COMPARISON
# ============================================================


plt.figure(
    figsize=(10,6)
)


plt.bar(
    results["model"],
    results["RMSE"]
)


plt.title(
    "Model Comparison - RMSE"
)


plt.ylabel(
    "RMSE (€/MWh)"
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


plt.savefig(
    f"{OUTPUT_DIR}/rmse_comparison.png",
    dpi=300
)


plt.close()



# ============================================================
# BEST MODEL
# ============================================================


best_model = results.loc[
    results["MAE"].idxmin()
]


print("\nBEST MODEL")

print(
    best_model
)



print("\nSaved files:")

print(
    "results/model_comparison.csv"
)

print(
    f"{OUTPUT_DIR}/mae_comparison.png"
)

print(
    f"{OUTPUT_DIR}/rmse_comparison.png"
)



print("\nDONE")