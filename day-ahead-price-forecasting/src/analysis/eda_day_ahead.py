import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ============================================================
# Paths
# ============================================================

DATA_PATH = (
    "data/final/germany/2020/"
    "germany_2020_full_dataset.csv"
)

OUTPUT_DIR = "reports/eda"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# Load dataset
# ============================================================

def load_data():

    print("="*60)
    print("Loading dataset")
    print("="*60)

    df = pd.read_csv(
        DATA_PATH,
        index_col="datetime",
        parse_dates=True
    )

    print(df.head())
    print()

    print("Shape:")
    print(df.shape)

    print()

    print("Missing values:")
    print(df.isna().sum().sort_values(ascending=False).head(10))

    return df



# ============================================================
# Price analysis
# ============================================================

def price_analysis(df):

    print("\n")
    print("="*60)
    print("Price statistics")
    print("="*60)

    print(
        df["price_eur_mwh"]
        .describe()
    )


    plt.figure(figsize=(12,5))

    plt.plot(
        df.index,
        df["price_eur_mwh"]
    )

    plt.title(
        "Germany Day Ahead Electricity Price 2020"
    )

    plt.ylabel(
        "EUR/MWh"
    )

    plt.xlabel(
        "Date"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/price_timeseries.png",
        dpi=300
    )

    plt.close()



# ============================================================
# Price distribution
# ============================================================

def price_distribution(df):

    plt.figure(figsize=(8,5))


    sns.histplot(
        df["price_eur_mwh"],
        bins=80,
        kde=True
    )


    plt.title(
        "Price Distribution"
    )


    plt.xlabel(
        "EUR/MWh"
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT_DIR}/price_distribution.png",
        dpi=300
    )


    plt.close()



# ============================================================
# Correlation
# ============================================================

def correlation_analysis(df):

    numeric = df.select_dtypes(
        include="number"
    )


    corr = (
        numeric
        .corr()
        ["price_eur_mwh"]
        .sort_values(
            ascending=False
        )
    )


    print("\nCorrelation with price:")
    print(corr)



    plt.figure(figsize=(12,10))


    sns.heatmap(
        numeric.corr(),
        cmap="coolwarm",
        center=0
    )


    plt.title(
        "Feature Correlation Matrix"
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT_DIR}/correlation_matrix.png",
        dpi=300
    )


    plt.close()



# ============================================================
# Generation mix
# ============================================================

def generation_analysis(df):


    generation_cols = [

        "Solar",
        "Wind Onshore",
        "Wind Offshore",
        "Biomass",
        "Nuclear",
        "Fossil Gas",
        "Fossil Brown coal/Lignite",
        "Fossil Hard coal"

    ]


    available = [
        c for c in generation_cols
        if c in df.columns
    ]


    monthly = (
        df[available]
        .mean()
    )


    plt.figure(figsize=(10,6))


    monthly.sort_values().plot(
        kind="barh"
    )


    plt.title(
        "Average Generation Mix 2020"
    )


    plt.xlabel(
        "MW"
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT_DIR}/generation_mix.png",
        dpi=300
    )


    plt.close()



# ============================================================
# Main
# ============================================================

def main():

    df = load_data()

    price_analysis(df)

    price_distribution(df)

    correlation_analysis(df)

    generation_analysis(df)


    print("\n")
    print("="*60)
    print("EDA COMPLETED")
    print("="*60)

    print(
        f"Reports saved in: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()