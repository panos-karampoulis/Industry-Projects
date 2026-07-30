import pandas as pd
import streamlit as st
import plotly.express as px

from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="European Energy Forecast Explorer",
    page_icon="⚡",
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


FORECAST_DIR = (
    DEMO_DIR
    /
    "forecasts"
    /
    "day_ahead"
)



MARKET_FILE = (
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
    "⚡ European Energy Forecast & Market Explorer"
)


st.markdown(
"""
Machine Learning based electricity market analytics platform.

Coverage:

🇩🇪 Germany  
🇫🇷 France  
🇮🇹 Italy  
🇳🇱 Netherlands  
🇪🇸 Spain  


Historical coverage:

**2020 - 2026**
"""
)



# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚡ Controls"
)



analysis_mode = st.sidebar.radio(

    "Analysis Mode",

    [

        "Forecast History",

        "Market History"

    ]

)



country = st.sidebar.selectbox(

    "Country",

    COUNTRIES

)



if st.sidebar.button(
    "🔄 Refresh Dashboard"
):

    st.rerun()



# ============================================================
# FORECAST HISTORY MODE
# ============================================================

if analysis_mode == "Forecast History":


    st.header(
        "📈 Day Ahead Forecast Explorer"
    )



    # --------------------------------------------------------
    # LOAD DEMO FORECAST FILE
    # --------------------------------------------------------


    forecast_file = (

        FORECAST_DIR

        /

        f"{country}_day_ahead_30d_forecast.csv"

    )



    if not forecast_file.exists():


        st.error(

            f"Missing forecast file:\n{forecast_file}"

        )


        st.stop()



    st.sidebar.success(

        f"{country.upper()} forecast loaded"

    )



    forecast = pd.read_csv(

        forecast_file

    )



    forecast["timestamp"] = pd.to_datetime(

        forecast["timestamp"],

        utc=True

    )



    forecast = forecast.sort_values(

        "timestamp"

    )



    # --------------------------------------------------------
    # FORECAST HORIZON
    # --------------------------------------------------------


    horizon = st.sidebar.selectbox(

        "Forecast Horizon",

        [

            "D+1 (Tomorrow)",

            "D+7",

            "D+14",

            "D+30"

        ]

    )



    forecast_start = (

        forecast["timestamp"]

        .min()

    )



    if horizon == "D+1 (Tomorrow)":


        end_date = (

            forecast_start

            +

            pd.Timedelta(days=1)

        )


    elif horizon == "D+7":


        end_date = (

            forecast_start

            +

            pd.Timedelta(days=7)

        )


    elif horizon == "D+14":


        end_date = (

            forecast_start

            +

            pd.Timedelta(days=14)

        )


    else:


        end_date = (

            forecast_start

            +

            pd.Timedelta(days=30)

        )



    forecast = forecast[

        forecast["timestamp"] < end_date

    ]



    if forecast.empty:


        st.warning(

            "No forecast data available"

        )


        st.stop()



    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------


    c1, c2, c3, c4 = st.columns(4)



    c1.metric(

        "Average Forecast",

        f"{forecast.forecast_price_eur_mwh.mean():.2f} €/MWh"

    )


    c2.metric(

        "Maximum",

        f"{forecast.forecast_price_eur_mwh.max():.2f} €/MWh"

    )


    c3.metric(

        "Minimum",

        f"{forecast.forecast_price_eur_mwh.min():.2f} €/MWh"

    )


    c4.metric(

        "Volatility",

        f"{forecast.forecast_price_eur_mwh.std():.2f}"

    )



    st.divider()



    # --------------------------------------------------------
    # FORECAST GRAPH
    # --------------------------------------------------------


    st.subheader(

        f"{country.upper()} {horizon} Forecast"

    )



    fig = px.line(

        forecast,

        x="timestamp",

        y="forecast_price_eur_mwh",

        markers=True

    )


    fig.update_layout(

        height=450,

        hovermode="x unified"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )



    st.subheader(

        "Forecast Data"

    )



    st.dataframe(

        forecast,

        use_container_width=True

    )

# ============================================================
# MARKET HISTORY MODE
# ============================================================

else:


    st.header(

        "📊 Historical Electricity Market Analysis"

    )



    # --------------------------------------------------------
    # CHECK MARKET DATA
    # --------------------------------------------------------


    if not MARKET_FILE.exists():


        st.error(

            f"Historical market dataset not found:\n{MARKET_FILE}"

        )


        st.stop()



    # --------------------------------------------------------
    # LOAD MARKET DATA
    # --------------------------------------------------------


    df = pd.read_csv(

        MARKET_FILE

    )



    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )



    # Filter country


    df = df[

        df["country"] == country

    ]



    df = df.sort_values(

        "timestamp"

    )



    if df.empty:


        st.warning(

            "No market data available for selected country"

        )


        st.stop()



    # --------------------------------------------------------
    # DATE RANGE
    # --------------------------------------------------------


    min_date = (

        df["timestamp"]

        .min()

        .date()

    )



    max_date = (

        df["timestamp"]

        .max()

        .date()

    )



    selected_date = st.sidebar.date_input(

        "Select Market Day",

        value=max_date,

        min_value=min_date,

        max_value=max_date

    )



    selected_date = pd.Timestamp(

        selected_date,

        tz="UTC"

    )



    next_day = (

        selected_date

        +

        pd.Timedelta(days=1)

    )



    daily_df = df[

        (df["timestamp"] >= selected_date)

        &

        (df["timestamp"] < next_day)

    ]



    if daily_df.empty:


        st.warning(

            "No data available for selected day"

        )


        st.stop()



    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "Average Price",

        f"{daily_df.price_eur_mwh.mean():.2f} €/MWh"

    )



    c2.metric(

        "Maximum",

        f"{daily_df.price_eur_mwh.max():.2f} €/MWh"

    )



    c3.metric(

        "Minimum",

        f"{daily_df.price_eur_mwh.min():.2f} €/MWh"

    )



    c4.metric(

        "Volatility",

        f"{daily_df.price_eur_mwh.std():.2f}"

    )



    st.divider()



    # --------------------------------------------------------
    # DAILY PRICE PROFILE
    # --------------------------------------------------------


    st.subheader(

        f"⚡ {country.upper()} Price Profile - {selected_date.date()}"

    )



    fig_daily = px.line(

        daily_df,

        x="timestamp",

        y="price_eur_mwh",

        markers=True

    )



    fig_daily.update_layout(

        height=450,

        hovermode="x unified"

    )



    st.plotly_chart(

        fig_daily,

        use_container_width=True

    )



    # --------------------------------------------------------
    # EXTREME EVENTS
    # --------------------------------------------------------


    st.subheader(

        "🚨 Extreme Price Events"

    )



    extreme_df = daily_df[

        (daily_df.price_eur_mwh < 0)

        |

        (daily_df.price_eur_mwh > 200)

    ]



    if extreme_df.empty:


        st.success(

            "No extreme price events detected"

        )


    else:


        st.dataframe(

            extreme_df,

            use_container_width=True

        )



    st.divider()



    # --------------------------------------------------------
    # MONTHLY AVERAGE
    # --------------------------------------------------------


    st.subheader(

        "📅 Monthly Average Price"

    )



    monthly = (

        df

        .set_index(

            "timestamp"

        )

        ["price_eur_mwh"]

        .resample(

            "ME"

        )

        .mean()

        .reset_index()

    )



    fig_month = px.bar(

        monthly,

        x="timestamp",

        y="price_eur_mwh",

        title=f"{country.upper()} Monthly Average Price"

    )



    fig_month.update_layout(

        height=400

    )



    st.plotly_chart(

        fig_month,

        use_container_width=True

    )



    # --------------------------------------------------------
    # CALENDAR HEATMAP
    # --------------------------------------------------------


    st.divider()



    st.subheader(

        "🗓️ Electricity Price Calendar Heatmap"

    )



    calendar_df = (

        df

        .set_index(

            "timestamp"

        )

        ["price_eur_mwh"]

        .resample(

            "D"

        )

        .mean()

        .reset_index()

    )



    calendar_df["year"] = (

        calendar_df["timestamp"]

        .dt.year

    )



    calendar_df["day_of_year"] = (

        calendar_df["timestamp"]

        .dt.dayofyear

    )



    heatmap_data = (

        calendar_df

        .pivot(

            index="year",

            columns="day_of_year",

            values="price_eur_mwh"

        )

    )



    fig_heatmap = px.imshow(

        heatmap_data,

        aspect="auto",

        labels={

            "x":"Day of Year",

            "y":"Year",

            "color":"€/MWh"

        },

        title=f"{country.upper()} Daily Average Electricity Prices"

    )



    fig_heatmap.update_layout(

        height=500

    )



    st.plotly_chart(

        fig_heatmap,

        use_container_width=True

    )



    # --------------------------------------------------------
    # SELECTED DAY DATA
    # --------------------------------------------------------


    st.divider()



    st.subheader(

        "📄 Selected Day Data"

    )



    st.dataframe(

        daily_df,

        use_container_width=True

    )

    
    
   