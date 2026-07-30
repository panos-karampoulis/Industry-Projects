import os
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="European Market Comparison",

    page_icon="🌍",

    layout="wide"

)



# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]


DEMO_DIR = (

    BASE_DIR

    /

    "demo_data"

)



DATA_FILE = (

    DEMO_DIR

    /

    "market"

    /

    "europe_intraday_prices.csv"

)



COUNTRIES = [

    "germany",

    "france",

    "italy",

    "netherlands",

    "spain"

]



# ============================================================
# TITLE
# ============================================================

st.title(

    "🌍 European Electricity Market Comparison"

)



st.markdown(

"""
Comparative analytics platform for European electricity markets.

Analyzed metrics:

- Average price
- Volatility
- Price extremes
- Negative prices
- Market correlation
- Market stress indicator
"""

)



# ============================================================
# DEBUG PATH CHECK
# ============================================================

with st.expander("🔍 Debug Information"):

    st.write("BASE DIR:", BASE_DIR)

    st.write("DATA FILE:", DATA_FILE)

    st.write("FILE EXISTS:", DATA_FILE.exists())



# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data

def load_market_data():


    df = pd.read_csv(

        DATA_FILE

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    df = df.sort_values(

        "timestamp"

    )


    return df



if not DATA_FILE.exists():


    st.error(

        f"""
Market dataset not found:

{DATA_FILE}

Please check demo_data/market folder.
"""

    )

    st.stop()



df = load_market_data()



df = df[

    df["country"].isin(COUNTRIES)

]



# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(

    "⚙️ Market Filters"

)



selected_countries = st.sidebar.multiselect(

    "Select Countries",

    COUNTRIES,

    default=COUNTRIES

)



if len(selected_countries) == 0:


    st.warning(

        "Select at least one country"

    )

    st.stop()



df = df[

    df["country"].isin(selected_countries)

]



# ============================================================
# MARKET KPI SUMMARY
# ============================================================

st.header(

    "📊 Market KPI Ranking"

)



summary = (

    df

    .groupby(

        "country"

    )

    .agg(

        Average_Price=(

            "price_eur_mwh",

            "mean"

        ),

        Volatility=(

            "price_eur_mwh",

            "std"

        ),

        Maximum_Price=(

            "price_eur_mwh",

            "max"

        ),

        Minimum_Price=(

            "price_eur_mwh",

            "min"

        ),

        Negative_Hours=(

            "price_eur_mwh",

            lambda x:

            int((x < 0).sum())

        )

    )

    .reset_index()

)



summary = summary.round(2)



st.dataframe(

    summary,

    use_container_width=True

)



# ============================================================
# AVERAGE PRICE RANKING
# ============================================================

st.divider()



st.subheader(

    "💶 Average Electricity Price Ranking"

)



price_rank = summary.sort_values(

    "Average_Price",

    ascending=False

)



fig_price = px.bar(

    price_rank,

    x="country",

    y="Average_Price",

    text="Average_Price",

    title="Average Electricity Price €/MWh"

)



fig_price.update_layout(

    height=400

)



st.plotly_chart(

    fig_price,

    use_container_width=True

)



# ============================================================
# VOLATILITY RANKING
# ============================================================

st.subheader(

    "⚠️ Electricity Market Volatility"

)



vol_rank = summary.sort_values(

    "Volatility",

    ascending=False

)



fig_vol = px.bar(

    vol_rank,

    x="country",

    y="Volatility",

    text="Volatility",

    title="Price Volatility (Standard Deviation)"

)



fig_vol.update_layout(

    height=400

)



st.plotly_chart(

    fig_vol,

    use_container_width=True

)



# ============================================================
# EXTREME PRICES
# ============================================================

st.divider()



st.subheader(

    "🚨 Extreme Price Events"

)



extreme = df[

    (df["price_eur_mwh"] < 0)

    |

    (df["price_eur_mwh"] > 200)

]



if extreme.empty:


    st.success(

        "No extreme events detected"

    )


else:


    st.dataframe(

        extreme.sort_values(

            "price_eur_mwh",

            ascending=False

        ).head(100),

        use_container_width=True

    )
# ============================================================
# PRICE CORRELATION MATRIX
# ============================================================

st.divider()



st.header(

    "🔗 Electricity Price Correlation"

)



pivot = (

    df

    .pivot_table(

        index="timestamp",

        columns="country",

        values="price_eur_mwh",

        aggfunc="mean"

    )

)



correlation = pivot.corr()



fig_corr = px.imshow(

    correlation,

    text_auto=True,

    aspect="auto",

    title="Market Price Correlation Matrix"

)



fig_corr.update_layout(

    height=500

)



st.plotly_chart(

    fig_corr,

    use_container_width=True

)



# ============================================================
# PRICE SPREAD ANALYSIS
# ============================================================

st.divider()



st.header(

    "📈 Market Spread Analysis"

)



available_markets = list(

    pivot.columns

)



if len(available_markets) >= 2:



    col1, col2 = st.columns(2)



    with col1:


        market_a = st.selectbox(

            "Market A",

            available_markets,

            index=0

        )



    with col2:


        market_b = st.selectbox(

            "Market B",

            available_markets,

            index=1

        )



    spread = (

        pivot[market_a]

        -

        pivot[market_b]

    )



    spread_df = pd.DataFrame(

        {

            "timestamp":

                spread.index,

            "spread_eur_mwh":

                spread.values

        }

    )



    fig_spread = px.line(

        spread_df,

        x="timestamp",

        y="spread_eur_mwh",

        title=(

            f"{market_a.upper()} - "

            f"{market_b.upper()} Price Spread"

        )

    )



    fig_spread.update_layout(

        height=450

    )



    st.plotly_chart(

        fig_spread,

        use_container_width=True

    )



# ============================================================
# MARKET STRESS SCORE
# ============================================================

st.divider()



st.header(

    "🚨 Market Stress Indicator"

)



stress = summary.copy()



# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------


max_volatility = stress["Volatility"].max()


max_negative = stress["Negative_Hours"].max()



if max_volatility == 0:

    max_volatility = 1



if max_negative == 0:

    max_negative = 1



stress["Volatility_Risk"] = (

    stress["Volatility"]

    /

    max_volatility

) * 50



stress["Negative_Price_Risk"] = (

    stress["Negative_Hours"]

    /

    max_negative

) * 50



stress["Stress_Score"] = (

    stress["Volatility_Risk"]

    +

    stress["Negative_Price_Risk"]

)



stress["Stress_Score"] = (

    stress["Stress_Score"]

    .round(0)

    .astype(int)

)



# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------


stress_table = stress[

    [

        "country",

        "Volatility",

        "Negative_Hours",

        "Stress_Score"

    ]

].sort_values(

    "Stress_Score",

    ascending=False

)



st.dataframe(

    stress_table,

    use_container_width=True

)



fig_stress = px.bar(

    stress_table,

    x="country",

    y="Stress_Score",

    text="Stress_Score",

    title="Electricity Market Stress Score (0-100)"

)



fig_stress.update_layout(

    height=400,

    yaxis_range=[0,100]

)



st.plotly_chart(

    fig_stress,

    use_container_width=True

)



# ============================================================
# FINAL MESSAGE
# ============================================================


st.success(

    "European Market Comparison Analysis Completed"

)