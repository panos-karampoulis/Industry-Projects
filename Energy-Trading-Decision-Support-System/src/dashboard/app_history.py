import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# Paths
# ==========================================

DECISION_PATH = (
    "data/decision/trading_decision_report.csv"
)


RISK_PATH = (
    "data/risk"
)



# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Energy Trading Decision Support System",
    page_icon="⚡",
    layout="wide"
)



# ==========================================
# Load Data
# ==========================================

@st.cache_data
def load_decision_data():

    df = pd.read_csv(
        DECISION_PATH
    )

    return df



@st.cache_data
def load_country_risk(country):

    path = (
        f"{RISK_PATH}/{country.lower()}_imbalance_risk.csv"
    )

    df = pd.read_csv(
        path
    )

    return df



df = load_decision_data()



# ==========================================
# Title
# ==========================================

st.title(
    "⚡ Energy Trading Decision Support System"
)


st.markdown(
    """
    AI-based analytics platform for electricity market
    risk assessment, imbalance forecasting and trading decisions.
    """
)



# ==========================================
# KPI Cards
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Markets monitored",
        len(df)
    )


with col2:

    st.metric(
        "Average Risk",
        round(
            df["avg_risk_score"].mean(),
            2
        )
    )


with col3:

    highest = df.loc[
        df["avg_risk_score"].idxmax(),
        "country"
    ]

    st.metric(
        "Highest Risk Market",
        highest
    )


with col4:

    st.metric(
        "High Risk Events",
        int(
            df["high_risk_events"].sum()
        )
    )



st.divider()



# ==========================================
# Market Ranking
# ==========================================

st.subheader(
    "📊 Market Risk Ranking"
)


st.dataframe(
    df[
        [
            "country",
            "avg_risk_score",
            "risk_category",
            "exposure_score",
            "confidence_score",
            "recommended_action"
        ]
    ],
    use_container_width=True
)



# ==========================================
# Risk Chart
# ==========================================

st.subheader(
    "🌍 Risk Comparison"
)


fig = px.bar(
    df,
    x="country",
    y="avg_risk_score",
    color="risk_category",
    title="Average Risk Score by Market"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================================
# Exposure Chart
# ==========================================

st.subheader(
    "📈 Trading Exposure Score"
)


fig2 = px.bar(
    df,
    x="country",
    y="exposure_score",
    color="country",
    title="Recommended Market Exposure"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# ==========================================
# Country Detail
# ==========================================

st.divider()

st.subheader(
    "🔎 Market Deep Dive"
)


country = st.selectbox(
    "Select market",
    df["country"].tolist()
)



risk_df = load_country_risk(
    country
)



col1, col2 = st.columns(2)



with col1:

    st.metric(
        "Average Imbalance MW",
        round(
            risk_df["imbalance_mw"].mean(),
            2
        )
    )


with col2:

    st.metric(
        "Maximum Imbalance MW",
        round(
            risk_df["imbalance_mw"].abs().max(),
            2
        )
    )



# Risk evolution

risk_df["timestamp"] = pd.to_datetime(
    risk_df["timestamp"]
)



fig3 = px.line(
    risk_df.tail(1000),
    x="timestamp",
    y="risk_score",
    title=f"{country} Risk Evolution"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)



# Imbalance distribution

fig4 = px.histogram(
    risk_df,
    x="imbalance_mw",
    nbins=50,
    title=f"{country} Imbalance Distribution"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)



# ==========================================
# Decision Box
# ==========================================

selected = df[
    df["country"] == country
].iloc[0]


st.divider()

st.subheader(
    "🤖 AI Trading Recommendation"
)



if selected["risk_category"] == "LOW":

    st.success(
        f"""
        Market: {country}

        Risk Level:
        LOW

        Recommendation:
        {selected['recommended_action']}

        Confidence:
        {selected['confidence_score']}%
        """
    )


elif selected["risk_category"] == "MEDIUM":

    st.warning(
        f"""
        Market: {country}

        Risk Level:
        MEDIUM

        Recommendation:
        {selected['recommended_action']}

        Confidence:
        {selected['confidence_score']}%
        """
    )


else:

    st.error(
        f"""
        Market: {country}

        Risk Level:
        HIGH

        Recommendation:
        {selected['recommended_action']}

        Confidence:
        {selected['confidence_score']}%
        """
    )