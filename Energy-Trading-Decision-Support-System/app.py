# ==========================================================
# ENERGY TRADING DECISION SUPPORT SYSTEM
# STREAMLIT DASHBOARD v5
# Cloud Demo + Local Compatible Version
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



DEMO_DIR = (

    BASE_DIR
    /
    "data"
    /
    "demo"

)



FEATURE_DIR = (

    BASE_DIR
    /
    "data"
    /
    "features"

)



RESULT_DIR = (

    BASE_DIR
    /
    "results"

)



PROCESSED_DIR = (

    BASE_DIR
    /
    "data"
    /
    "processed"

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
# LOAD FEATURES
# ==========================================================


@st.cache_data
def load_features(country):


    """
    Priority:

    1. Demo dataset (Cloud)
    2. Local dataset

    """


    demo_file = (

        DEMO_DIR

        /

        f"{country}_features_sample.csv"

    )



    local_file = (

        FEATURE_DIR

        /

        f"{country}_features.csv"

    )



    if demo_file.exists():

        file = demo_file


        mode = "Demo"


    elif local_file.exists():

        file = local_file


        mode = "Local"


    else:


        st.error(

            f"Dataset missing for {country}"

        )

        st.stop()



    df = pd.read_csv(file)



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df, mode





# ==========================================================
# LOAD MARKET PRICES
# ==========================================================


@st.cache_data
def load_prices(country, market):


    """
    Load additional market prices.

    If missing:
    use day_ahead_price from features.

    """


    if market == "Day Ahead":


        filename = (

            f"{country}_day_ahead_prices.csv"

        )


    else:


        filename = (

            f"{country}_intraday_prices.csv"

        )



    local_file = (

        PROCESSED_DIR

        /

        filename

    )



    if not local_file.exists():


        return pd.DataFrame()



    df = pd.read_csv(local_file)



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df





# ==========================================================
# LOAD RISK DATA
# ==========================================================


@st.cache_data
def load_risk(country):


    """
    Priority:

    Demo risk
    Local results

    """


    demo_file = (

        DEMO_DIR

        /

        "imbalance_risk_sample.csv"

    )



    local_file = (

        RESULT_DIR

        /

        f"{country}_imbalance_risk.csv"

    )



    if demo_file.exists():


        df = pd.read_csv(

            demo_file

        )


    elif local_file.exists():


        df = pd.read_csv(

            local_file

        )


    else:


        return pd.DataFrame()



    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            utc=True

        )



    return df





# ==========================================================
# LOAD TRADING SIGNALS
# ==========================================================


@st.cache_data
def load_signals():


    """
    Priority:

    Demo signals
    Local results

    """


    demo_file = (

        DEMO_DIR

        /

        "trading_decisions_sample.csv"

    )



    local_file = (

        RESULT_DIR

        /

        "trading_decisions_all_countries.csv"

    )



    if demo_file.exists():


        df = pd.read_csv(

            demo_file

        )


    elif local_file.exists():


        df = pd.read_csv(

            local_file

        )


    else:


        return pd.DataFrame()



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



st.sidebar.divider()



# ==========================================================
# DATA MODE DISPLAY
# ==========================================================


features_check = (

    DEMO_DIR

    /

    f"{country}_features_sample.csv"

)



if features_check.exists():

    st.sidebar.success(

        "🔵 Demo Dataset Mode"

    )

else:

    st.sidebar.info(

        "🟢 Local Dataset Mode"

    )





# ==========================================================
# PIPELINE BUTTON
# ==========================================================


st.sidebar.divider()



if st.sidebar.button(

    "🔄 Refresh Pipeline"

):


    with st.spinner(

        "Running pipeline..."

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


features, data_mode = load_features(

    country

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
# CLEAN MARKET DATA
# ==========================================================


market = features.copy()



# ----------------------------------------------------------
# Add optional market price
# ----------------------------------------------------------


if not prices.empty:


    if (

        "price_eur_mwh"

        in

        prices.columns

    ):


        prices = prices.rename(

            columns={

                "price_eur_mwh":

                "market_price"

            }

        )



    if "market_price" in prices.columns:


        market = market.merge(

            prices[

                [

                    "timestamp",

                    "market_price"

                ]

            ],

            on="timestamp",

            how="left"

        )



else:


    market["market_price"] = market.get(

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
# DAILY DATA
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


    if "country" in signals.columns:


        signal_day = signals[

            (

                signals["country"]

                ==

                country

            )

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



else:


    signal_day = pd.DataFrame()






# ==========================================================
# LATEST VALUES
# ==========================================================


latest = market_day.iloc[-1]




if not signal_day.empty:


    latest_signal = signal_day.iloc[-1]


else:


    latest_signal = {


        "trading_signal":

        "N/A",


        "confidence":

        0,


        "risk_score":

        0


    }






# ==========================================================
# TITLE
# ==========================================================


st.title(

    "⚡ Energy Trading Decision Support System"

)



st.caption(

f"""

Day Ahead & Intraday Market Analysis |

Load Forecasting |

Renewable Generation |

Imbalance Risk |

Trading Signals


Dataset Mode:

{data_mode}

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

        "market_price",

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



if "market_price" in market_day.columns:


    price_columns.append(

        "market_price"

    )





if price_columns:


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

        "Price data unavailable"

    )







# ==========================================================
# SYSTEM FUNDAMENTALS
# ==========================================================


st.subheader(

    "⚡ System Fundamentals"

)



col1, col2 = st.columns(2)






# -----------------------------
# LOAD
# -----------------------------


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







# -----------------------------
# RENEWABLES
# -----------------------------


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
# IMBALANCE RISK ANALYTICS
# ==========================================================


st.subheader(

    "⚠️ Imbalance Risk Analytics"

)





if not risk.empty:



    risk_country = risk[


        risk["country"]

        ==

        country


    ]



    risk_day = risk_country[


        risk_country["timestamp"]

        .dt.date

        ==

        selected_date


    ]




    if not risk_day.empty:



        fig = px.line(

            risk_day,

            x="timestamp",

            y="risk_score",

            title="Imbalance Risk Score (0-10)"

        )



        st.plotly_chart(

            fig,

            use_container_width=True

        )




        latest_risk = (

            risk_day

            .iloc[-1]

            ["risk_score"]

        )




        if latest_risk < 3:


            risk_level = "LOW"



        elif latest_risk < 7:


            risk_level = "MEDIUM"



        else:


            risk_level = "HIGH"




        st.metric(

            "Current Risk Level",

            risk_level,

            f"{latest_risk:.2f}"

        )



    else:


        st.info(

            "No risk data for selected date"

        )



else:


    st.info(

        "Risk data unavailable"

    )








# ==========================================================
# TRADING DECISION ENGINE
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

            "No signals available"

        )


else:


    st.info(

        "Trading decisions unavailable"

    )







# ==========================================================
# AI RECOMMENDATION
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

{data_mode}

"""

)