import pandas as pd

from feature_engineering import create_features


# -------------------------
# Load Italy generation
# -------------------------

df = pd.read_csv(
    "data/processed/italy/italy_generation.csv",
    parse_dates=[
        "datetime"
    ]
)


print("Loaded:")
print(df.shape)



# -------------------------
# Create features
# -------------------------

features = create_features(
    df,
    country="italy",
    save=True
)

print()
print("Feature dataset created")
print(features.shape)