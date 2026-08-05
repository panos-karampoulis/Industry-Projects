# ==========================================================
# PAGE 6
# TRADING STRATEGY BACKTESTING PERFORMANCE
# Cloud + Local Compatible
# ==========================================================


import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np

from pathlib import Path



# ==========================================================
# CONFIG
# ==========================================================


st.set_page_config(

    page_title="Backtesting Performance",

    page_icon="📊",

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



METRICS_FILE = (

    RESULT_DIR

    /

    "strategy_metrics.json"

)




# ==========================================================
# LOAD BACKTEST
# ==========================================================


@st.cache_data
def load_backtest():



    if BACKTEST_FILE.exists():


        df = pd.read_csv(

            BACKTEST_FILE

        )


        mode="Local"



    else:


        demo_file = (

            DEMO_DIR

            /

            "trading_decisions_sample.csv"

        )


        df = pd.read_csv(

            demo_file

        )


        mode="Demo"




    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )



    # ------------------------------
    # CREATE DEMO PNL
    # ------------------------------


    if "hourly_pnl" not in df.columns:


        np.random.seed(42)


        df["hourly_pnl"] = (

            np.random.normal(

                500,

                3000,

                len(df)

            )

        )



    if "position_change" not in df.columns:


        df["position_change"] = (

            np.random.choice(

                [-1,0,1],

                len(df)

            )

        )



    if "equity_curve" not in df.columns:


        df = df.sort_values(

            "timestamp"

        )


        df["equity_curve"] = (

            df["hourly_pnl"]

            .cumsum()

        )



    return df, mode





# ==========================================================
# METRICS
# ==========================================================


@st.cache_data
def load_metrics(backtest):


    if METRICS_FILE.exists():


        with open(

            METRICS_FILE,

            "r"

        ) as f:


            data=json.load(f)



        df=pd.DataFrame(data).T.reset_index()


        df=df.rename(

            columns={

                "index":"country"

            }

        )


        return df



    # ------------------------------
    # DEMO METRICS
    # ------------------------------


    rows=[]


    for c in backtest.country.unique():


        temp=backtest[

            backtest.country==c

        ]


        pnl=temp.hourly_pnl.sum()



        rows.append(

            {


            "country":c,


            "total_pnl_eur":pnl,


            "sharpe_ratio":0.85,


            "profit_factor":1.45


            }

        )


    return pd.DataFrame(rows)




# ==========================================================
# DATA
# ==========================================================


backtest, mode = load_backtest()


metrics = load_metrics(

    backtest

)



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(

    "📊 Backtesting Controls"

)



selected_country = st.sidebar.selectbox(

    "Country",

    sorted(

        backtest.country.unique()

    )

)




country_all = backtest[

    backtest.country==selected_country

].copy()



min_date=country_all.timestamp.min().date()


max_date=country_all.timestamp.max().date()



selected_date=st.sidebar.date_input(

    "Analysis Date",

    value=max_date,

    min_value=min_date,

    max_value=max_date

)




country_day = country_all[

    country_all.timestamp.dt.date

    ==

    selected_date

]




if country_day.empty:

    country_day=country_all.tail(24)




country_metrics = metrics[

    metrics.country==selected_country

].iloc[0]





daily_pnl = country_day.hourly_pnl.sum()


daily_trades = (

    country_day.position_change

    .abs()

    .sum()

)




# ==========================================================
# TITLE
# ==========================================================


st.title(

    "📊 Trading Strategy Backtesting & PnL Analytics"

)



st.caption(

f"""

Mode: {mode}

Historical trading strategy simulation

"""

)



# ==========================================================
# KPI
# ==========================================================


c1,c2,c3,c4,c5=st.columns(5)



with c1:

    st.metric(

        "Daily PnL",

        f"{daily_pnl:,.0f} €"

    )


with c2:

    st.metric(

        "Total PnL",

        f"{country_metrics.total_pnl_eur:,.0f} €"

    )


with c3:

    st.metric(

        "Sharpe Ratio",

        f"{country_metrics.sharpe_ratio:.2f}"

    )


with c4:

    st.metric(

        "Profit Factor",

        f"{country_metrics.profit_factor:.2f}"

    )


with c5:

    st.metric(

        "Trades",

        int(daily_trades)

    )



st.divider()



# ==========================================================
# PNL
# ==========================================================


st.subheader(

    "💰 Intraday PnL"

)



fig=px.bar(

    country_day,

    x="timestamp",

    y="hourly_pnl"

)


st.plotly_chart(

    fig,

    use_container_width=True

)




# ==========================================================
# SIGNALS
# ==========================================================


st.subheader(

    "📈 Trading Signals"

)



if "trading_signal" in country_day.columns:


    counts=(

        country_day.trading_signal

        .value_counts()

        .reset_index()

    )


    counts.columns=[

        "signal",

        "count"

    ]



    fig=px.pie(

        counts,

        names="signal",

        values="count"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




# ==========================================================
# EQUITY CURVE
# ==========================================================


st.subheader(

    "📈 Equity Curve"

)



fig=px.line(

    country_all,

    x="timestamp",

    y="equity_curve"

)



st.plotly_chart(

    fig,

    use_container_width=True

)




# ==========================================================
# RANKING
# ==========================================================


st.subheader(

    "🌍 Country Ranking"

)



ranking=metrics.sort_values(

    "total_pnl_eur",

    ascending=False

)



fig=px.bar(

    ranking,

    x="country",

    y="total_pnl_eur",

    color="country"

)



st.plotly_chart(

    fig,

    use_container_width=True

)


st.dataframe(

    ranking,

    use_container_width=True

)