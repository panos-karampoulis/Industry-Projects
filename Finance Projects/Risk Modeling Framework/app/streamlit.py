import streamlit as st
import sys
import os
import pandas as pd


# =========================
# Project Path
# =========================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(PROJECT_ROOT)


# =========================
# Imports
# =========================

from src.data import load_prices

from src.returns import (
    calculate_returns,
    calculate_portfolio_returns
)

from src.historical_var import (
    historical_var
)

from src.parametric_var import (
    parametric_var
)

from src.monte_carlo_var import (
    monte_carlo_var
)

from src.expected_shortfall import (
    expected_shortfall
)

from src.risk_report import (
    create_risk_report
)

from src.stress_analysis import (
    worst_loss_days
)


from src.stress_testing import stress_test

from src.crisis_analysis import analyze_crisis

from src.plotting import (
    plot_return_distribution,
    plot_cumulative_returns
)

from src.plotting import (
    plot_return_distribution,
    plot_cumulative_returns,
    plot_drawdown
)


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Risk Modeling Framework",
    page_icon="📉",
    layout="wide"
)


st.title(
    "📉 Risk Modeling Framework"
)

st.write(
    """
    Value at Risk, Monte Carlo Simulation,
    Expected Shortfall and Risk Analytics Dashboard
    """
)


# =========================
# Load Data
# =========================

@st.cache_data
def load_data():

    path = os.path.join(
        PROJECT_ROOT,
        "data",
        "raw",
        "prices.csv"
    )

    return load_prices(path)



prices = load_data()



# =========================
# Returns
# =========================

returns = calculate_returns(
    prices
)



# Equal Weight Portfolio

n_assets = prices.shape[1]


weights = [
    1/n_assets
] * n_assets



portfolio_returns = calculate_portfolio_returns(
    returns,
    weights
)



# =========================
# Sidebar
# =========================

st.sidebar.header(
    "Risk Parameters"
)


portfolio_value = st.sidebar.number_input(
    "Portfolio Value (€)",
    value=100000
)


confidence = st.sidebar.selectbox(
    "Confidence Level",
    [
        0.95,
        0.99
    ]
)



# =========================
# Risk Calculations
# =========================

hist_var = historical_var(
    portfolio_returns,
    confidence
)


param_var = parametric_var(
    portfolio_returns,
    confidence
)


mc_var = monte_carlo_var(
    portfolio_returns,
    confidence
)


es = expected_shortfall(
    portfolio_returns,
    confidence
)



# Euro Values

hist_amount = (
    hist_var *
    portfolio_value
)


param_amount = (
    param_var *
    portfolio_value
)


mc_amount = (
    mc_var *
    portfolio_value
)


es_amount = (
    es *
    portfolio_value
)



# =========================
# KPI Cards
# =========================

st.subheader(
    "Risk Overview"
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Historical VaR",
    f"€{hist_amount:,.0f}"
)


col2.metric(
    "Parametric VaR",
    f"€{param_amount:,.0f}"
)


col3.metric(
    "Monte Carlo VaR",
    f"€{mc_amount:,.0f}"
)


col4.metric(
    "Expected Shortfall",
    f"€{es_amount:,.0f}"
)



# =========================
# Risk Report
# =========================

st.subheader(
    "Risk Comparison"
)


risk_report = create_risk_report(

    historical_var(
        portfolio_returns,
        0.95
    ),

    historical_var(
        portfolio_returns,
        0.99
    ),


    parametric_var(
        portfolio_returns,
        0.95
    ),

    parametric_var(
        portfolio_returns,
        0.99
    ),


    monte_carlo_var(
        portfolio_returns,
        0.95
    ),

    monte_carlo_var(
        portfolio_returns,
        0.99
    ),


    expected_shortfall(
        portfolio_returns,
        0.95
    ),

    expected_shortfall(
        portfolio_returns,
        0.99
    ),


    portfolio_value

)


st.dataframe(
    risk_report,
    use_container_width=True
)



# =========================
# VaR Chart
# =========================

import plotly.express as px


fig_var = px.bar(
    risk_report,
    x="Metric",
    y="95%",
    title="95% Risk Measure Comparison"
)


st.plotly_chart(
    fig_var,
    use_container_width=True
)



# =========================
# Return Distribution
# =========================

st.subheader(
    "Return Distribution"
)


fig_distribution = plot_return_distribution(
    portfolio_returns,
    hist_var,
    es
)


st.plotly_chart(
    fig_distribution,
    use_container_width=True
)



# =========================
# Portfolio Growth
# =========================

st.subheader(
    "Portfolio Growth"
)


fig_growth = plot_cumulative_returns(
    portfolio_returns
)


st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# =========================
# Drawdown Analysis
# =========================

st.subheader(
    "Portfolio Drawdown Analysis"
)


fig_drawdown = plot_drawdown(
    portfolio_returns
)


st.plotly_chart(
    fig_drawdown,
    use_container_width=True
)

# =========================
# Worst Loss Days
# =========================

st.subheader(
    "Worst Historical Loss Days"
)


worst = worst_loss_days(
    portfolio_returns,
    portfolio_value,
    n_days=10
)


st.dataframe(
    worst,
    use_container_width=True
)


# =========================
# Stress Testing
# =========================


st.subheader(
    "Stress Testing Scenarios"
)


stress_results = stress_test(
    portfolio_value
)


st.dataframe(
    stress_results,
    use_container_width=True
)



fig_stress = px.bar(

    stress_results,

    x="Scenario",

    y="Portfolio Impact (€)",

    title="Portfolio Stress Impact"

)


st.plotly_chart(
    fig_stress,
    use_container_width=True
)

# =========================
# Historical Crisis
# =========================

st.subheader(
    "Historical Crisis Replay"
)


crisis_choice = st.selectbox(

    "Select Crisis",

    [
        "COVID Crash",
        "2022 Rate Shock"
    ]

)



if crisis_choice == "COVID Crash":

    crisis_result = analyze_crisis(
        portfolio_returns,
        "2020-02-01",
        "2020-04-30"
    )


else:

    crisis_result = analyze_crisis(
        portfolio_returns,
        "2022-01-01",
        "2022-12-31"
    )



if crisis_result:

    crisis_df = pd.DataFrame(
        crisis_result.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


    st.dataframe(
        crisis_df,
        use_container_width=True
    )

# =========================
# Download Reports
# =========================

st.subheader(
    "Export Reports"
)


csv = risk_report.to_csv(
    index=False
)


st.download_button(
    label="⬇ Download Risk Report CSV",
    data=csv,
    file_name="risk_report.csv",
    mime="text/csv"
)