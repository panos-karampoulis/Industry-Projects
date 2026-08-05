# ==========================================================
# PAGE 7
# TRADE ANALYTICS
# Cloud + Local Compatible
# ==========================================================


import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from pathlib import Path



# ==========================================================
# CONFIG
# ==========================================================


st.set_page_config(

    page_title="Trade Analytics",

    page_icon="📈",

    layout="wide"

)



BASE_DIR = Path(__file__).resolve().parents[1]


RESULT_DIR = BASE_DIR / "results"


DEMO_DIR = (
    BASE_DIR
    /
    "data"
    /
    "demo"
)



BACKTEST_FILE = (

    RESULT_DIR

    /

    "backtest_results.csv"

)



# ==========================================================
# LOAD DATA
# ==========================================================


@st.cache_data
def load_data():



    if BACKTEST_FILE.exists():


        df = pd.read_csv(

            BACKTEST_FILE

        )

        mode="Local"



    else:


        demo_file=(

            DEMO_DIR

            /

            "trading_decisions_sample.csv"

        )


        df=pd.read_csv(

            demo_file

        )

        mode="Demo"




    df["timestamp"]=pd.to_datetime(

        df["timestamp"],

        utc=True

    )



    # --------------------------------
    # CREATE REQUIRED FIELDS
    # --------------------------------


    if "hourly_pnl" not in df.columns:


        np.random.seed(42)


        df["hourly_pnl"]=np.random.normal(

            500,

            3000,

            len(df)

        )




    if "position_change" not in df.columns:


        df["position_change"]=np.random.choice(

            [-1,0,1],

            len(df)

        )



    if "trading_signal" not in df.columns:


        df["trading_signal"]="HOLD"



    if "risk_level" not in df.columns:


        df["risk_level"]="MEDIUM"



    return df,mode





df,mode=load_data()



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "📈 Trade Analytics"

)


countries=sorted(

    df.country.unique()

)



country=st.sidebar.selectbox(

    "Country",

    [

        "All"

    ]

    +

    countries

)



if country!="All":


    data=df[

        df.country==country

    ].copy()


else:

    data=df.copy()




# ==========================================================
# TITLE
# ==========================================================


st.title(

    "📈 Trading Strategy Analytics"

)



st.caption(

f"""

Detailed analysis of trading signals,

risk levels and PnL behaviour.


Mode: {mode}

"""

)




# ==========================================================
# KPI
# ==========================================================


c1,c2,c3,c4=st.columns(4)



with c1:


    st.metric(

        "Total PnL",

        f"{data.hourly_pnl.sum():,.0f} €"

    )



with c2:


    st.metric(

        "Trades",

        int(

            data.position_change.abs().sum()

        )

    )



with c3:


    st.metric(

        "Average Trade PnL",

        f"{data.hourly_pnl.mean():,.0f} €"

    )



with c4:


    win_rate=(

        data.hourly_pnl.gt(0)

        .mean()

        *

        100

    )


    st.metric(

        "Win Rate",

        f"{win_rate:.1f}%"

    )




st.divider()



# ==========================================================
# SIGNAL PERFORMANCE
# ==========================================================


st.subheader(

    "🎯 PnL by Trading Signal"

)



signal_pnl=(

    data

    .groupby(

        "trading_signal"

    )

    ["hourly_pnl"]

    .sum()

    .reset_index()

)



fig=px.bar(

    signal_pnl,

    x="trading_signal",

    y="hourly_pnl",

    color="trading_signal"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==========================================================
# RISK
# ==========================================================


st.subheader(

    "⚠️ PnL by Risk Level"

)



risk_pnl=(

    data

    .groupby(

        "risk_level"

    )

    ["hourly_pnl"]

    .sum()

    .reset_index()

)



fig=px.bar(

    risk_pnl,

    x="risk_level",

    y="hourly_pnl",

    color="risk_level"

)



st.plotly_chart(

    fig,

    use_container_width=True

)




# ==========================================================
# HOURLY PERFORMANCE
# ==========================================================


st.subheader(

    "⏰ Performance by Hour"

)



data["hour"]=data.timestamp.dt.hour



hour_perf=(

    data

    .groupby(

        "hour"

    )

    ["hourly_pnl"]

    .sum()

    .reset_index()

)



fig=px.bar(

    hour_perf,

    x="hour",

    y="hourly_pnl",

    title="Hourly PnL"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# ==========================================================
# BEST / WORST
# ==========================================================


col1,col2=st.columns(2)



with col1:


    st.subheader(

        "🏆 Best Hours"

    )


    st.dataframe(

        hour_perf.sort_values(

            "hourly_pnl",

            ascending=False

        )

        .head(5),

        hide_index=True

    )




with col2:


    st.subheader(

        "📉 Worst Hours"

    )


    st.dataframe(

        hour_perf.sort_values(

            "hourly_pnl",

            ascending=True

        )

        .head(5),

        hide_index=True

    )





# ==========================================================
# COUNTRY COMPARISON
# ==========================================================


if country=="All":


    st.divider()


    st.subheader(

        "🌍 Country PnL Comparison"

    )



    country_perf=(

        df

        .groupby(

            "country"

        )

        ["hourly_pnl"]

        .sum()

        .reset_index()

    )



    fig=px.bar(

        country_perf,

        x="country",

        y="hourly_pnl",

        color="country"

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )