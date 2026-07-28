import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Market Explorer",

    page_icon="⚡",

    layout="wide"

)



# ============================================================
# TITLE
# ============================================================

st.title(
    "⚡ Energy Market Explorer"
)


st.markdown(
"""
Historical analysis and forecasting overlay of day-ahead electricity markets
(2020-2026)
"""
)



# ============================================================
# LOAD DATA
# ============================================================


@st.cache_data
def load_market_data(country):


    file = (

        Path("data")

        /

        "processed"

        /

        country

        /

        f"{country}_clean.csv"

    )


    df = pd.read_csv(

        file,

        index_col=0,

        parse_dates=True

    )


    df.index = pd.to_datetime(

        df.index,

        utc=True

    )


    df = df.sort_index()


    return df




# ============================================================
# ENERGY FEATURE ENGINEERING
# ============================================================


def create_energy_features(df):


    df = df.copy()


    renewable_keywords = [

        "solar",
        "wind",
        "hydro",
        "biomass"

    ]


    renewable_cols = [

        col for col in df.columns

        if any(

            key in col.lower()

            for key in renewable_keywords

        )

    ]


    if renewable_cols:


        df["renewable_generation"] = (

            df[renewable_cols]

            .sum(axis=1)

        )


    else:


        df["renewable_generation"] = 0



    fossil_keywords = [

        "gas",
        "lignite",
        "coal",
        "oil"

    ]


    fossil_cols = [

        col for col in df.columns

        if any(

            key in col.lower()

            for key in fossil_keywords

        )

    ]



    if fossil_cols:


        df["fossil_generation"] = (

            df[fossil_cols]

            .sum(axis=1)

        )


    else:


        df["fossil_generation"] = 0



    df["residual_load"] = (

        df["load_mw"]

        -

        df["renewable_generation"]

    )


    df["renewable_share"] = (

        df["renewable_generation"]

        /

        df["load_mw"]

        *

        100

    ).replace(

        [np.inf, -np.inf],

        0

    )


    return df




# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(
    "⚙️ Market Settings"
)



country = st.sidebar.selectbox(

    "Country",

    [

        "germany",

        "greece"

    ]

)



df = load_market_data(

    country

)


df = create_energy_features(

    df

)



st.sidebar.success(

    f"{country.upper()} loaded"

)



# ============================================================
# ANALYSIS MODE
# ============================================================


mode = st.sidebar.radio(

    "Analysis Mode",

    [

        "📅 Single Day",

        "📈 Historical Period"

    ]

)



# ============================================================
# SINGLE DAY FILTER
# ============================================================


if mode == "📅 Single Day":


    available_dates = (

        pd.Series(

            df.index.date

        )

        .unique()

        .tolist()

    )


    selected_date = st.sidebar.date_input(

        "📅 Select Date",

        value=available_dates[-1],

        min_value=min(available_dates),

        max_value=max(available_dates)

    )


    data = df[

        df.index.date == selected_date

    ].copy()



# ============================================================
# HISTORICAL PERIOD FILTER
# ============================================================


else:


    start_date, end_date = st.sidebar.date_input(

        "📅 Select Period",

        [

            df.index.date.min(),

            df.index.date.max()

        ],

        min_value=df.index.date.min(),

        max_value=df.index.date.max()

    )


    data = df[

        (df.index.date >= start_date)

        &

        (df.index.date <= end_date)

    ].copy()



if data.empty:


    st.warning(

        "No data available for selected period"

    )


    st.stop()

# ============================================================
# KPI SECTION
# ============================================================


st.subheader(

    f"📊 Market Summary | {country.upper()}"

)



col1, col2, col3, col4 = st.columns(4)



col1.metric(

    "Average Price",

    f"{data['price_eur_mwh'].mean():.2f} €/MWh"

)



col2.metric(

    "Maximum Price",

    f"{data['price_eur_mwh'].max():.2f} €/MWh"

)



col3.metric(

    "Minimum Price",

    f"{data['price_eur_mwh'].min():.2f} €/MWh"

)



col4.metric(

    "Renewable Share",

    f"{data['renewable_share'].mean():.1f}%"

)




# ============================================================
# PRICE EVOLUTION
# ============================================================


st.subheader(

    "⚡ Electricity Price Evolution"

)



fig_price = go.Figure()



fig_price.add_trace(

    go.Scatter(

        x=data.index,

        y=data["price_eur_mwh"],

        mode="lines",

        name="Electricity Price"

    )

)



fig_price.update_layout(

    height=450,

    xaxis_title="Date",

    yaxis_title="€/MWh",

    hovermode="x unified"

)



st.plotly_chart(

    fig_price,

    use_container_width=True

)





# ============================================================
# DEMAND
# ============================================================


st.subheader(

    "🔌 Electricity Demand"

)



fig_load = go.Figure()



fig_load.add_trace(

    go.Scatter(

        x=data.index,

        y=data["load_mw"],

        mode="lines",

        name="Load MW"

    )

)



fig_load.update_layout(

    height=400,

    xaxis_title="Date",

    yaxis_title="MW",

    hovermode="x unified"

)



st.plotly_chart(

    fig_load,

    use_container_width=True

)





# ============================================================
# RENEWABLE GENERATION
# ============================================================


st.subheader(

    "🌱 Renewable Generation"

)



fig_renew = go.Figure()



fig_renew.add_trace(

    go.Scatter(

        x=data.index,

        y=data["renewable_generation"],

        mode="lines",

        name="Renewable Generation"

    )

)



fig_renew.update_layout(

    height=400,

    xaxis_title="Date",

    yaxis_title="MW",

    hovermode="x unified"

)



st.plotly_chart(

    fig_renew,

    use_container_width=True

)





# ============================================================
# RESIDUAL LOAD
# ============================================================


st.subheader(

    "⚡ Residual Load"

)



fig_residual = go.Figure()



fig_residual.add_trace(

    go.Scatter(

        x=data.index,

        y=data["residual_load"],

        mode="lines",

        name="Residual Load"

    )

)



fig_residual.update_layout(

    height=400,

    xaxis_title="Date",

    yaxis_title="MW",

    hovermode="x unified"

)



st.plotly_chart(

    fig_residual,

    use_container_width=True

)

# ============================================================
# ENERGY MIX
# ============================================================


st.subheader(
    "⚡ Energy Generation Mix"
)



generation_keywords = [

    "solar",
    "wind",
    "hydro",
    "biomass",
    "gas",
    "lignite",
    "coal",
    "oil"

]



generation_cols = [

    col for col in data.columns

    if any(

        key in col.lower()

        for key in generation_keywords

    )

]



fig_mix = go.Figure()



for col in generation_cols:


    fig_mix.add_trace(

        go.Scatter(

            x=data.index,

            y=data[col],

            mode="lines",

            stackgroup="one",

            name=col

        )

    )



fig_mix.update_layout(

    height=500,

    xaxis_title="Date",

    yaxis_title="MW",

    hovermode="x unified"

)



st.plotly_chart(

    fig_mix,

    use_container_width=True

)





# ============================================================
# FORECAST OVERLAY
# ============================================================


st.subheader(
    "🤖 Forecast Overlay"
)



show_forecast = st.checkbox(

    "Show CatBoost Forecast"

)



if show_forecast:


    forecast_file = Path(

        f"results/{country}/catboost_predictions.csv"

    )


    if forecast_file.exists():


        forecast = pd.read_csv(

            forecast_file

        )


        forecast["datetime"] = pd.to_datetime(

            forecast["Unnamed: 0"],

            utc=True

        )


        forecast = forecast.sort_values(

            "datetime"

        )



        overlay = data.merge(

            forecast[

                [

                    "datetime",

                    "catboost_prediction"

                ]

            ],

            left_index=True,

            right_on="datetime",

            how="inner"

        )



        if not overlay.empty:


            fig_forecast = go.Figure()



            fig_forecast.add_trace(

                go.Scatter(

                    x=overlay["datetime"],

                    y=overlay["price_eur_mwh"],

                    mode="lines",

                    name="Actual Price"

                )

            )



            fig_forecast.add_trace(

                go.Scatter(

                    x=overlay["datetime"],

                    y=overlay["catboost_prediction"],

                    mode="lines",

                    name="CatBoost Forecast"

                )

            )



            fig_forecast.update_layout(

                height=450,

                xaxis_title="Date",

                yaxis_title="€/MWh",

                hovermode="x unified"

            )



            st.plotly_chart(

                fig_forecast,

                use_container_width=True

            )



            # Forecast metrics


            mae = (

                overlay["price_eur_mwh"]

                -

                overlay["catboost_prediction"]

            ).abs().mean()



            rmse = np.sqrt(

                (

                    overlay["price_eur_mwh"]

                    -

                    overlay["catboost_prediction"]

                )

                .pow(2)

                .mean()

            )



            col1, col2 = st.columns(2)



            col1.metric(

                "Forecast MAE",

                f"{mae:.2f} €/MWh"

            )



            col2.metric(

                "Forecast RMSE",

                f"{rmse:.2f} €/MWh"

            )


        else:


            st.info(

                "Forecast available only from test period (2025-04 onwards)."

            )


    else:


        st.warning(

            "CatBoost prediction file not available."

        )





# ============================================================
# EXPORT
# ============================================================


st.subheader(

    "📥 Export Market Data"

)



csv = data.to_csv().encode(

    "utf-8"

)



st.download_button(

    label="Download Selected Market Data",

    data=csv,

    file_name=(

        f"{country}_market_export.csv"

    ),

    mime="text/csv"

)