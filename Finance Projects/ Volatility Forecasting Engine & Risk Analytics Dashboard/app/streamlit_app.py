import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="Volatility Forecasting Engine",
    layout="wide"
)


# ---------------------------------
# Load data
# ---------------------------------

model_results = pd.read_csv(
    "results/volatility_model_results.csv"
)


var_results = pd.read_csv(
    "results/var_results.csv"
)


garch_params = pd.read_csv(
    "results/garch_parameters.csv"
)


market_data = pd.read_csv(
    "data/SPY_processed_data.csv",
    index_col=0,
    parse_dates=True
)


garch_forecast = pd.read_csv(
    "data/garch_rolling_forecast.csv",
    index_col=0,
    parse_dates=True
)


# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title(
    "Navigation"
)


page = st.sidebar.selectbox(
    "Go to",
    [
        "Overview",
        "Volatility Models",
        "Risk Analytics",
        "Model Insights"
    ]
)


# ---------------------------------
# Overview
# ---------------------------------

if page == "Overview":

    st.title(
        "Volatility Forecasting Engine"
    )


    st.markdown(
        """
        Quantitative finance dashboard for volatility
        forecasting and risk analytics.

        Models:
        - Historical volatility
        - EWMA
        - GARCH(1,1)

        Risk models:
        - Historical VaR
        - Parametric VaR
        - GARCH-based VaR
        """
    )


    st.divider()


    latest_price = market_data["Close"].iloc[-1]

    latest_return = market_data["Returns"].iloc[-1]

    latest_volatility = garch_forecast.iloc[-1,0]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Latest Price",
            f"{latest_price:.2f}"
        )


    with col2:

        st.metric(
            "Latest Return",
            f"{latest_return:.2%}"
        )


    with col3:

        st.metric(
            "GARCH Volatility",
            f"{latest_volatility:.2%}"
        )


    st.divider()


    st.subheader(
        "Price History"
    )


    price_chart = px.line(
        market_data,
        y="Close",
        title="SPY Price Evolution"
    )


    st.plotly_chart(
        price_chart,
        use_container_width=True
    )



# ---------------------------------
# Volatility Models
# ---------------------------------

elif page == "Volatility Models":

    st.title(
        "Volatility Model Comparison"
    )


    st.subheader(
        "Forecasting Performance"
    )


    st.dataframe(
        model_results,
        use_container_width=True
    )


    rmse_chart = px.bar(
        model_results,
        x="Model",
        y="RMSE",
        title="RMSE Comparison"
    )


    st.plotly_chart(
        rmse_chart,
        use_container_width=True
    )


    mae_chart = px.bar(
        model_results,
        x="Model",
        y="MAE",
        title="MAE Comparison"
    )


    st.plotly_chart(
        mae_chart,
        use_container_width=True
    )


    st.divider()


    st.subheader(
        "Realized Volatility vs GARCH Forecast"
    )


    volatility_data = pd.concat(
        [
            market_data["Rolling_Volatility"],
            garch_forecast.iloc[:,0]
        ],
        axis=1
    )


    volatility_data.columns = [
        "Realized",
        "GARCH"
    ]


    volatility_chart = px.line(
        volatility_data,
        title="Volatility Forecast Comparison"
    )


    st.plotly_chart(
        volatility_chart,
        use_container_width=True
    )



# ---------------------------------
# Risk Analytics
# ---------------------------------

elif page == "Risk Analytics":

    st.title(
        "Risk Analytics - Value at Risk"
    )


    st.subheader(
        "VaR Results"
    )


    st.dataframe(
        var_results,
        use_container_width=True
    )


    violation_chart = px.bar(
        var_results,
        x="Method",
        y="Violation_Rate",
        title="VaR Backtesting Violation Rate"
    )


    st.plotly_chart(
        violation_chart,
        use_container_width=True
    )


    st.info(
        """
        For a 95% VaR model, approximately 5%
        violations are expected.

        GARCH-based VaR achieved the closest
        calibration to the expected level.
        """
    )


    st.divider()


    st.subheader(
        "Daily Returns Distribution"
    )


    return_chart = px.histogram(
        market_data,
        x="Returns",
        nbins=100,
        title="Return Distribution"
    )


    st.plotly_chart(
        return_chart,
        use_container_width=True
    )



# ---------------------------------
# Model Insights
# ---------------------------------

elif page == "Model Insights":

    st.title(
        "Model Interpretation"
    )


    st.markdown(
        """
        ## Volatility Forecasting

        The historical volatility benchmark achieved
        the lowest forecasting error.

        GARCH provided a dynamic framework capable of
        modelling volatility clustering.


        ## Risk Analytics

        Static VaR approaches were more conservative.

        GARCH-based VaR achieved violation rates close
        to the expected 5% confidence level.


        ## Main Conclusion

        Forecast accuracy and risk calibration represent
        different objectives.

        A model with higher forecasting error can still
        provide better risk management results.
        """
    )


    st.subheader(
        "GARCH Parameters"
    )


    st.dataframe(
        garch_params,
        use_container_width=True
    )