import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="AI Investment Decision Engine",
    page_icon="📈",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"


# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_data():

    metrics = pd.read_csv(
        DATA_DIR / "performance_metrics.csv",
        index_col=0
    )

    equity = pd.read_csv(
        DATA_DIR / "equity_curves.csv",
        index_col=0,
        parse_dates=True
    )

    ml_signals = pd.read_csv(
        DATA_DIR / "ml_signals.csv"
    )

    feature_importance = pd.read_csv(
        DATA_DIR / "feature_importance.csv"
    )

    shap_values = pd.read_csv(
        DATA_DIR / "shap_values.csv"
    )


    return (
        metrics,
        equity,
        ml_signals,
        feature_importance,
        shap_values
    )


(
    metrics,
    equity,
    ml_signals,
    feature_importance,
    shap_values
) = load_data()



# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "AI Investment Engine"
)


page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Portfolio",
        "🤖 ML Signals",
        "🧠 Explainability",
        "📈 Backtest",
        "ℹ️ About"
    ]
)



# =========================
# HEADER
# =========================

st.title(
    "AI Investment Decision Engine"
)

st.caption(
    "Machine Learning powered equity selection & portfolio analytics"
)



# =========================
# PORTFOLIO PAGE
# =========================

if page == "📊 Portfolio":


    st.subheader(
        "AI Portfolio KPIs"
    )


    ai = metrics.loc[
        "AI Portfolio"
    ]


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Annual Return",
        f"{ai['Annual Return']:.2%}"
    )


    c2.metric(
        "Sharpe Ratio",
        f"{ai['Sharpe Ratio']:.2f}"
    )


    c3.metric(
        "Volatility",
        f"{ai['Annual Volatility']:.2%}"
    )


    c4.metric(
        "Max Drawdown",
        f"{ai['Maximum Drawdown']:.2%}"
    )


    st.divider()


    st.subheader(
        "Performance Metrics"
    )


    st.dataframe(
        metrics.style.format(
            "{:.2%}"
        ),
        use_container_width=True
    )



# =========================
# BACKTEST PAGE
# =========================

elif page == "📈 Backtest":


    st.subheader(
        "Equity Curve"
    )


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=equity.index,
            y=equity["AI Portfolio"],
            name="AI Portfolio"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=equity.index,
            y=equity["SPY"],
            name="SPY"
        )
    )


    fig.update_layout(
        height=500,
        yaxis_title="Growth of $1",
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.subheader(
        "Drawdown"
    )


    ai_dd = (
        equity["AI Portfolio"]
        /
        equity["AI Portfolio"].cummax()
    ) - 1


    spy_dd = (
        equity["SPY"]
        /
        equity["SPY"].cummax()
    ) - 1



    fig2 = go.Figure()


    fig2.add_trace(
        go.Scatter(
            x=ai_dd.index,
            y=ai_dd,
            name="AI Portfolio"
        )
    )


    fig2.add_trace(
        go.Scatter(
            x=spy_dd.index,
            y=spy_dd,
            name="SPY"
        )
    )


    fig2.update_layout(
        height=500,
        yaxis_title="Drawdown",
        template="plotly_white"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# =========================
# ML PAGE
# =========================

elif page == "🤖 ML Signals":


    st.subheader(
        "ML Stock Ranking"
    )


    def color_signal(row):

        if row["Signal"] == "BUY":
            return [
                "background-color:#90EE90"
            ] * len(row)

        return [
            "background-color:#FFFACD"
        ] * len(row)



    st.dataframe(
        ml_signals.style.apply(
            color_signal,
            axis=1
        ),
        use_container_width=True
    )


    st.subheader(
        "Feature Importance"
    )


    fi = feature_importance.sort_values(
        "Importance"
    )


    fig = go.Figure(
        go.Bar(
            x=fi["Importance"],
            y=fi["Feature"],
            orientation="h"
        )
    )


    fig.update_layout(
        height=600,
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =========================
# SHAP PAGE
# =========================

elif page == "🧠 Explainability":


    st.subheader(
        "Why did the model choose this stock?"
    )


    stock = st.selectbox(
        "Select Stock",
        shap_values["symbol"].unique()
    )


    values = (
        shap_values[
            shap_values["symbol"] == stock
        ]
        .drop(
            columns=["symbol"]
        )
        .T
    )


    values.columns=[
        "SHAP"
    ]


    values = values.sort_values(
        "SHAP"
    )


    fig = go.Figure(
        go.Bar(
            x=values["SHAP"],
            y=values.index,
            orientation="h"
        )
    )


    fig.update_layout(
        height=600,
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =========================
# ABOUT
# =========================

elif page == "ℹ️ About":


    st.write(
        """
        ## AI Investment Decision Engine

        Features:

        - Financial data pipeline
        - ML stock classification
        - Portfolio backtesting
        - Risk analytics
        - SHAP explainability

        Built with:

        - Python
        - Pandas
        - Scikit-Learn
        - SHAP
        - Streamlit
        """
    )