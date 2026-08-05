# ==========================================================
# ENERGY TRADING DECISION SUPPORT SYSTEM
# STREAMLIT DASHBOARD v4
# Cloud + Local Compatible Version
# ==========================================================


import streamlit as st
import pandas as pd
import plotly.express as px

import subprocess
import sys

from pathlib import Path
from datetime import datetime



# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(

    page_title="Energy Trading DSS",

    page_icon="⚡",

    layout="wide"

)



# ==========================================================
# PATHS
# ==========================================================


BASE_DIR = Path(__file__).resolve().parent



# Real datasets

FEATURE_DIR = (

    BASE_DIR

    /

    "data"

    /

    "features"

)



PRICE_DIR = (

    BASE_DIR

    /

    "data"

    /

    "processed"

)



# Demo datasets for Streamlit Cloud

DEMO_DIR = (

    BASE_DIR

    /

    "data"

    /

    "demo"

)



RESULT_DIR = (

    BASE_DIR

    /

    "results"

)



MODELS_DIR = (

    BASE_DIR

    /

    "models"

)




PIPELINE = [

    sys.executable,

    "src/pipeline/run_pipeline.py"

]




COUNTRIES = [

    "germany",

    "france",

    "italy",

    "spain",

    "netherlands"

]



# ==========================================================
# DATA LOADING FUNCTIONS
# ==========================================================


@st.cache_data
def load_features(country):


    """
    Load feature dataset.

    Priority:
    1. Real local dataset
    2. Demo dataset for Cloud deployment
    """



    real_file = (

        FEATURE_DIR

        /

        f"{country}_features.csv"

    )



    demo_file = (

        DEMO_DIR

        /

        f"{country}_features_sample.csv"

    )




    if real_file.exists():

        file = real_file


    elif demo_file.exists():

        file = demo_file


    else:


        st.error(

            f"No feature dataset found for {country}"

        )

        st.stop()




    df = pd.read_csv(file)

    # Keep only price columns

    keep_columns = [
        "timestamp",
        "price_eur_mwh",
        "day_ahead_price",
        "intraday_price"
    ]


    df = df[
        [
            c for c in keep_columns
            if c in df.columns
        ]
    ]



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df






@st.cache_data
def load_prices(country, market):


    """
    Load market prices.

    Local:
        data/processed/

    Cloud:
        demo/features sample fallback

    """



    if market == "Day Ahead":


        real_file = (

            PRICE_DIR

            /

            f"{country}_day_ahead_prices.csv"

        )


    else:


        real_file = (

            PRICE_DIR

            /

            f"{country}_intraday_prices.csv"

        )




    demo_file = (

        DEMO_DIR

        /

        f"{country}_features_sample.csv"

    )




    if real_file.exists():

        file = real_file



    elif demo_file.exists():

        file = demo_file



    else:

        return pd.DataFrame()



    df = pd.read_csv(file)




    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )




    if "price_eur_mwh" in df.columns:


        df = df.rename(

            columns={

                "price_eur_mwh": market

            }

        )



    elif market not in df.columns:


        if "day_ahead_price" in df.columns and market=="Day Ahead":

            df[market] = df["day_ahead_price"]


        elif "intraday_price" in df.columns and market=="Intraday":

            df[market] = df["intraday_price"]



    return df







@st.cache_data
def load_risk(country):


    file = (

        RESULT_DIR

        /

        f"{country}_imbalance_risk.csv"

    )



    if not file.exists():

        return pd.DataFrame()



    df = pd.read_csv(file)



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df






@st.cache_data
def load_signals():


    file = (

        RESULT_DIR

        /

        "trading_decisions_all_countries.csv"

    )



    if not file.exists():

        return pd.DataFrame()



    df = pd.read_csv(file)



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df
# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "⚡ Energy Trading DSS"

)




country = st.sidebar.selectbox(

    "Country",

    COUNTRIES

)




market_type = st.sidebar.selectbox(

    "Price Market",

    [

        "Day Ahead",

        "Intraday"

    ]

)




# ==========================================================
# DATA MODE INFORMATION
# ==========================================================


st.sidebar.divider()



real_available = (

    FEATURE_DIR

    /

    f"{country}_features.csv"

).exists()



if real_available:


    st.sidebar.success(

        "🟢 Local Data Available"

    )


else:


    st.sidebar.info(

        "🔵 Demo Data Mode"

    )





# ==========================================================
# PIPELINE REFRESH
# ==========================================================


st.sidebar.divider()



if st.sidebar.button(

    "🔄 Refresh Pipeline"

):


    with st.spinner(

        "Running complete pipeline..."

    ):



        try:


            result = subprocess.run(

                PIPELINE,

                cwd=BASE_DIR,

                capture_output=True,

                text=True

            )



            if result.returncode == 0:


                st.sidebar.success(

                    "Pipeline completed"

                )



                st.cache_data.clear()


                st.rerun()



            else:


                st.sidebar.error(

                    "Pipeline failed"

                )


                st.sidebar.code(

                    result.stderr

                )



        except Exception as e:


            st.sidebar.error(

                str(e)

            )






# ==========================================================
# LOAD DATA
# ==========================================================


features = load_features(

    country

)


st.write("DEBUG COUNTRY:", country)

st.write(
    "DEBUG SHAPE:",
    features.shape
)

st.write(
    "DEBUG COLUMNS:",
    features.columns.tolist()
)

st.write(
    features.head()
)

prices = load_prices(

    country,

    market_type

)




risk = load_risk(

    country

)




signals = load_signals()





# ==========================================================
# MERGE MARKET DATA
# ==========================================================



market = features.copy()


st.write("FINAL MARKET COLUMNS")
st.write(market.columns.tolist())


if not prices.empty:


    if "day_ahead_price" not in market.columns:


        market = market.merge(

            prices,

            on="timestamp",

            how="left"

        )

else:


    market[market_type] = market.get(

        "day_ahead_price",

        0

    )






# ==========================================================
# DATE SELECTOR
# ==========================================================


min_date = (

    market["timestamp"]

    .min()

    .date()

)



max_date = (

    market["timestamp"]

    .max()

    .date()

)




selected_date = st.sidebar.date_input(

    "Select Date",

    value=max_date,

    min_value=min_date,

    max_value=max_date

)






# ==========================================================
# DAILY FILTER
# ==========================================================


market_day = market[

    market["timestamp"]

    .dt.date

    ==

    selected_date

]





if market_day.empty:


    market_day = market.tail(96)






# ==========================================================
# SIGNAL FILTER
# ==========================================================



if not signals.empty:


    signal_day = signals[

        (signals["country"] == country)

        &

        (

            signals["timestamp"]

            .dt.date

            ==

            selected_date

        )

    ]


else:


    signal_day = pd.DataFrame()






# ==========================================================
# LATEST VALUES
# ==========================================================


latest = market_day.iloc[-1]

st.write("DEBUG MARKET DAY SHAPE:", market_day.shape)

st.write("DEBUG LATEST ROW:")
st.write(latest)

st.write(
    "DEBUG LOAD VALUE:",
    latest.get("load_mw")
)

st.write(
    "DEBUG RENEWABLE VALUE:",
    latest.get("renewable_share")
)



if not signal_day.empty:


    latest_signal = signal_day.iloc[-1]



else:


    latest_signal = {


        "trading_signal": "N/A",


        "confidence": 0,


        "risk_score": 0


    }







# ==========================================================
# TITLE
# ==========================================================


st.title(

    "⚡ Energy Trading Decision Support System"

)



st.caption(

"""

Day Ahead & Intraday Market Analysis |

Load Forecasting |

Renewable Generation |

Imbalance Risk |

Trading Signals

"""

)






# ==========================================================
# KPI SECTION
# ==========================================================



c1,c2,c3,c4,c5 = st.columns(5)






with c1:


    price = latest.get(

        "day_ahead_price",

        0

    )


    st.metric(

        "Day Ahead Price",

        f"{price:.2f} €/MWh"

    )







with c2:


    market_price = latest.get(

        market_type,

        0

    )


    st.metric(

        market_type,

        f"{market_price:.2f} €/MWh"

    )







with c3:


    load = latest.get(

        "load_mw",

        0

    )


    st.metric(

        "Load",

        f"{load:.0f} MW"

    )






with c4:


    renewable = latest.get(

        "renewable_share",

        0

    )


    st.metric(

        "Renewable Share",

        f"{renewable:.1%}"

    )







with c5:


    st.metric(

        "Trading Signal",

        latest_signal.get(

            "trading_signal",

            "N/A"

        )

    )





st.divider()

# ==========================================================
# PRICE ANALYSIS
# ==========================================================


st.subheader(

    "📈 Market Price Analysis"

)




price_columns = []



if "day_ahead_price" in market_day.columns:

    price_columns.append(

        "day_ahead_price"

    )



if market_type in market_day.columns:

    price_columns.append(

        market_type

    )





if len(price_columns) > 0:


    fig = px.line(

        market_day,

        x="timestamp",

        y=price_columns,

        title="Electricity Market Prices"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


else:


    st.info(

        "Price data not available"

    )





# ==========================================================
# SYSTEM FUNDAMENTALS
# ==========================================================


st.subheader(

    "⚡ System Fundamentals"

)




col1,col2 = st.columns(2)






with col1:


    if "load_mw" in market_day.columns:


        fig = px.line(

            market_day,

            x="timestamp",

            y="load_mw",

            title="Electricity Load Forecast"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(

            "Load data unavailable"

        )







with col2:


    renewable_columns = []



    for col in [

        "wind_generation",

        "solar_generation",

        "renewable_generation"

    ]:


        if col in market_day.columns:


            renewable_columns.append(

                col

            )





    if renewable_columns:


        fig = px.area(

            market_day,

            x="timestamp",

            y=renewable_columns,

            title="Renewable Generation"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:


        st.info(

            "Renewable data unavailable"

        )






# ==========================================================
# IMBALANCE RISK
# ==========================================================


st.subheader(

    "⚠️ Imbalance Risk Analytics"

)





if not risk.empty:



    risk_day = risk[

        risk["timestamp"]

        .dt.date

        ==

        selected_date

    ]



    if not risk_day.empty:


        fig = px.line(

            risk_day,

            x="timestamp",

            y="risk_score",

            title="Imbalance Risk Score"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



        latest_risk = risk_day.iloc[-1]["risk_score"]



        if latest_risk < 0.33:


            risk_label = "Low Risk"



        elif latest_risk < 0.66:


            risk_label = "Medium Risk"



        else:


            risk_label = "High Risk"




        st.metric(

            "Current Risk Level",

            risk_label,

            f"{latest_risk:.2f}"

        )



    else:


        st.info(

            "No risk data for selected date"

        )



else:


    st.info(

        "Risk results available after running local pipeline"

    )







# ==========================================================
# TRADING SIGNAL ANALYSIS
# ==========================================================


st.subheader(

    "💹 Trading Decision Engine"

)






if not signals.empty:



    country_signals = signals[

        signals["country"]

        ==

        country

    ]



    if not country_signals.empty:


        fig = px.pie(

            country_signals,

            names="trading_signal",

            title=f"{country} Trading Signal Distribution"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



else:


    st.info(

        "Trading decisions available after pipeline execution"

    )






# ==========================================================
# FINAL RECOMMENDATION
# ==========================================================


st.divider()



st.subheader(

    "🤖 AI Trading Recommendation"

)





signal = latest_signal.get(

    "trading_signal",

    "N/A"

)



confidence = latest_signal.get(

    "confidence",

    0

)



risk_score = latest_signal.get(

    "risk_score",

    0

)





if signal == "BUY":


    color = "green"



elif signal == "SELL":


    color = "red"



else:


    color = "orange"





st.markdown(

f"""

<h2 style="color:{color}">

Recommendation: {signal}

</h2>


<b>Confidence:</b>

{confidence:.1f}%


<br>


<b>Risk Score:</b>

{risk_score:.2f}


""",

unsafe_allow_html=True

)







# ==========================================================
# FOOTER
# ==========================================================


st.divider()



st.caption(

f"""

Dashboard refresh:

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


Mode:

{"Local Data" if real_available else "Demo Data"}

"""

)