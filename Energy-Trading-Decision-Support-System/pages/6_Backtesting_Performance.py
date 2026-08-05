# ==========================================================
# PAGE 6
# TRADING STRATEGY BACKTESTING PERFORMANCE
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import json

from pathlib import Path



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]


RESULT_DIR = (
    BASE_DIR /
    "results"
)


BACKTEST_FILE = (
    RESULT_DIR /
    "backtest_results.csv"
)


METRICS_FILE = (
    RESULT_DIR /
    "strategy_metrics.json"
)



# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Backtesting Performance",

    page_icon="📊",

    layout="wide"

)



# ==========================================================
# LOAD DATA
# ==========================================================


@st.cache_data
def load_backtest():


    df = pd.read_csv(

        BACKTEST_FILE

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        utc=True

    )


    return df




@st.cache_data
def load_metrics():


    with open(

        METRICS_FILE,

        "r"

    ) as f:

        data = json.load(f)



    metrics = pd.DataFrame(data).T.reset_index()


    metrics = metrics.rename(

        columns={

            "index":"country"

        }

    )


    return metrics





# ==========================================================
# LOAD
# ==========================================================


backtest = load_backtest()

metrics = load_metrics()



countries = sorted(

    backtest["country"]
    .unique()

)



# ==========================================================
# SIDEBAR
# ==========================================================


st.sidebar.title(
    "📊 Backtesting Controls"
)



selected_country = st.sidebar.selectbox(

    "Country",

    countries

)



country_all = backtest[

    backtest["country"]

    ==

    selected_country

].copy()



min_date = (

    country_all["timestamp"]

    .min()

    .date()

)


max_date = (

    country_all["timestamp"]

    .max()

    .date()

)



selected_date = st.sidebar.date_input(

    "Analysis Date",

    value=max_date,

    min_value=min_date,

    max_value=max_date

)



# ==========================================================
# FILTER SELECTED DAY
# ==========================================================


country_day = country_all[

    country_all["timestamp"]

    .dt.date

    ==

    selected_date

].copy()



if country_day.empty:


    st.warning(

        "No data available for selected date"

    )


    st.stop()





country_metrics = metrics[

    metrics["country"]

    ==

    selected_country

].iloc[0]



daily_pnl = (

    country_day["hourly_pnl"]

    .sum()

)



daily_trades = (

    country_day["position_change"]
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

"""
Historical strategy evaluation based on generated trading signals.
PnL simulation, performance metrics and country comparison.
"""

)




st.subheader(

    f"{selected_country.upper()} - {selected_date}"

)





# ==========================================================
# KPI CARDS
# ==========================================================


c1,c2,c3,c4,c5 = st.columns(5)



with c1:

    st.metric(

        "Selected Day PnL",

        f"{daily_pnl:,.2f} €"

    )



with c2:

    st.metric(

        "Total Strategy PnL",

        f"{country_metrics.total_pnl_eur:,.2f} €"

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

        "Trades Today",

        daily_trades

    )





st.divider()



# ==========================================================
# DAILY PNL TIMELINE
# ==========================================================


st.subheader(

    "💰 Intraday PnL"

)



fig = px.bar(

    country_day,

    x="timestamp",

    y="hourly_pnl",

    title="Hourly Profit / Loss"

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


    signal_count = (

        country_day["trading_signal"]

        .value_counts()

        .reset_index()

    )


    signal_count.columns=[

        "Signal",

        "Count"

    ]



    fig = px.pie(

        signal_count,

        names="Signal",

        values="Count",

        title="BUY / SELL / HOLD Distribution"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )





# ==========================================================
# EQUITY CURVE
# ==========================================================


st.subheader(

    "📈 Full Strategy Equity Curve"

)



fig = px.line(

    country_all,

    x="timestamp",

    y="equity_curve",

    title=f"{selected_country.upper()} Equity Curve"

)


st.plotly_chart(

    fig,

    use_container_width=True

)





# ==========================================================
# COUNTRY COMPARISON
# ==========================================================


st.divider()



st.subheader(

    "🌍 Country Performance Ranking"

)



ranking = metrics.sort_values(

    "total_pnl_eur",

    ascending=False

)



fig = px.bar(

    ranking,

    x="country",

    y="total_pnl_eur",

    color="country",

    title="Total Portfolio PnL"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



st.dataframe(

    ranking,

    use_container_width=True,

    hide_index=True

)