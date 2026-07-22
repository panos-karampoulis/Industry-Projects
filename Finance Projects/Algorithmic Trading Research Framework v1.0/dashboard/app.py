import sys
from pathlib import Path

import streamlit as st

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# Project Path
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# =====================================================
# Framework Imports
# =====================================================

from app.data_loader import load_market_data

from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)

from app.backtester import run_backtest

from app.portfolio import combine_strategies

from app.walk_forward import walk_forward_analysis



# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(

    page_title="Algorithmic Trading Research Framework",

    page_icon="📈",

    layout="wide"

)



# =====================================================
# Helper Functions
# =====================================================


def calculate_sharpe(returns):

    std = returns.std()

    if std == 0:

        return 0

    return (
        returns.mean()
        /
        std
        *
        np.sqrt(252)
    )



def calculate_annual_return(returns):

    equity = (
        1 + returns
    ).cumprod()

    years = len(returns) / 252

    if years == 0:

        return 0

    return (
        equity.iloc[-1]
        **
        (1 / years)
        -
        1
    )



def calculate_volatility(returns):

    return (
        returns.std()
        *
        np.sqrt(252)
    )



def calculate_drawdown(returns):

    equity = (
        1 + returns
    ).cumprod()


    running_max = (
        equity.cummax()
    )


    drawdown = (
        equity /
        running_max
        -
        1
    )


    return drawdown.min()



def calculate_sortino(returns):

    negative_returns = returns[
        returns < 0
    ]


    downside = negative_returns.std()


    if downside == 0:

        return 0


    return (

        returns.mean()
        /
        downside
        *
        np.sqrt(252)

    )



def calculate_calmar(returns):

    annual = calculate_annual_return(
        returns
    )

    dd = abs(
        calculate_drawdown(
            returns
        )
    )


    if dd == 0:

        return 0


    return annual / dd



def calculate_win_rate(returns):

    return (
        (returns > 0).sum()
        /
        len(returns)
    )



def create_equity_curve(returns):

    return (
        1 + returns
    ).cumprod()



def risk_contribution(returns):

    volatility = returns.std()


    if volatility.sum() == 0:

        return volatility


    return (
        volatility /
        volatility.sum()
    )



def return_contribution(returns):

    avg_return = returns.mean()


    if avg_return.sum() == 0:

        return avg_return


    return (
        avg_return /
        avg_return.sum()
    )



# =====================================================
# Header
# =====================================================

st.title(
    "📈 Algorithmic Trading Research Framework"
)


st.markdown(
"""
Quantitative research dashboard for systematic trading strategies.

Modules:

- Technical Indicators
- Strategy Backtesting
- Portfolio Construction
- Risk Analytics
- Walk Forward Validation
"""
)



# =====================================================
# Sidebar
# =====================================================

st.sidebar.header(
    "⚙ Configuration"
)



asset = st.sidebar.selectbox(

    "Asset",

    [
        "AAPL",
        "MSFT",
        "TSLA",
        "NVDA"
    ]

)



strategies_selected = st.sidebar.multiselect(

    "Strategies",

    [

        "SMA Crossover",

        "RSI Mean Reversion",

        "Momentum"

    ],

    default=[

        "SMA Crossover",

        "RSI Mean Reversion",

        "Momentum"

    ]

)



run = st.sidebar.button(
    "🚀 Run Analysis"
)



# =====================================================
# Main Execution
# =====================================================

if run:


    with st.spinner(
        "Running analysis..."
    ):


        # -----------------------------
        # Load Data
        # -----------------------------

        df = load_market_data(
            asset
        )


        df = build_indicators(
            df
        )


        portfolios = {}

        strategy_returns = {}



        # -----------------------------
        # SMA
        # -----------------------------

        if "SMA Crossover" in strategies_selected:


            sma_signal = sma_crossover_strategy(
                df
            )


            sma_portfolio = run_backtest(

                df["Close"],

                sma_signal

            )


            portfolios["SMA"] = sma_portfolio


            strategy_returns["SMA"] = (
                sma_portfolio.returns()
            )



        # -----------------------------
        # RSI
        # -----------------------------

        if "RSI Mean Reversion" in strategies_selected:


            rsi_signal = rsi_mean_reversion(
                df
            )


            rsi_portfolio = run_backtest(

                df["Close"],

                rsi_signal

            )


            portfolios["RSI"] = rsi_portfolio


            strategy_returns["RSI"] = (
                rsi_portfolio.returns()
            )



        # -----------------------------
        # Momentum
        # -----------------------------

        if "Momentum" in strategies_selected:


            momentum_signal = momentum_strategy(
                df
            )


            momentum_portfolio = run_backtest(

                df["Close"],

                momentum_signal

            )


            portfolios["Momentum"] = momentum_portfolio


            strategy_returns["Momentum"] = (
                momentum_portfolio.returns()
            )



        returns_df = pd.DataFrame(
            strategy_returns
        )



        combined_returns = combine_strategies(
            returns_df
        )


        equity = create_equity_curve(
            combined_returns
        )

        
        # =====================================================
        # Portfolio Metrics
        # =====================================================

        total_return = (
            equity.iloc[-1] - 1
        )


        annual_return = calculate_annual_return(
            combined_returns
        )


        volatility = calculate_volatility(
            combined_returns
        )


        sharpe = calculate_sharpe(
            combined_returns
        )


        sortino = calculate_sortino(
            combined_returns
        )


        calmar = calculate_calmar(
            combined_returns
        )


        max_drawdown = calculate_drawdown(
            combined_returns
        )


        win_rate = calculate_win_rate(
            combined_returns
        )



        # =====================================================
        # Tabs
        # =====================================================

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(

            [

                "📊 Overview",

                "📈 Strategies",

                "⚠️ Risk Analytics",

                "💼 Portfolio",

                "🔬 Walk Forward",

                "📥 Reports"

            ]

        )



        # =====================================================
        # TAB 1 - Overview
        # =====================================================

        with tab1:


            st.subheader(
                "Portfolio Performance"
            )


            c1, c2, c3, c4 = st.columns(4)


            c1.metric(

                "Total Return",

                f"{total_return:.2%}"

            )


            c2.metric(

                "Annual Return",

                f"{annual_return:.2%}"

            )


            c3.metric(

                "Sharpe Ratio",

                f"{sharpe:.2f}"

            )


            c4.metric(

                "Maximum Drawdown",

                f"{max_drawdown:.2%}"

            )


            c5, c6, c7, c8 = st.columns(4)


            c5.metric(

                "Volatility",

                f"{volatility:.2%}"

            )


            c6.metric(

                "Sortino Ratio",

                f"{sortino:.2f}"

            )


            c7.metric(

                "Calmar Ratio",

                f"{calmar:.2f}"

            )


            c8.metric(

                "Win Rate",

                f"{win_rate:.2%}"

            )


            st.divider()



            # Equity Curve

            st.subheader(
                "Equity Curve"
            )


            fig = go.Figure()



            fig.add_trace(

                go.Scatter(

                    x=equity.index,

                    y=equity,

                    mode="lines",

                    name="Portfolio"

                )

            )


            fig.update_layout(

                height=450,

                template="plotly_white"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



            # Drawdown

            st.subheader(
                "Drawdown Curve"
            )


            drawdown = (

                equity /

                equity.cummax()

                -

                1

            )



            fig = go.Figure()



            fig.add_trace(

                go.Scatter(

                    x=drawdown.index,

                    y=drawdown,

                    fill="tozeroy",

                    name="Drawdown"

                )

            )


            fig.update_layout(

                height=400,

                template="plotly_white"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )




        # =====================================================
        # TAB 2 - Strategies
        # =====================================================

        with tab2:


            st.subheader(
                "Strategy Comparison"
            )


            comparison = []



            for name, portfolio in portfolios.items():


                strategy_ret = portfolio.returns()



                comparison.append(

                    {

                    "Strategy":

                    name,


                    "Return":

                    strategy_ret.add(1).prod()-1,


                    "Sharpe":

                    calculate_sharpe(strategy_ret),


                    "Drawdown":

                    calculate_drawdown(strategy_ret)

                    }

                )



            comparison_df = pd.DataFrame(
                comparison
            )



            st.dataframe(

                comparison_df.style.format(

                    {

                    "Return":"{:.2%}",

                    "Sharpe":"{:.2f}",

                    "Drawdown":"{:.2%}"

                    }

                ),

                use_container_width=True

            )



            fig = px.bar(

                comparison_df,

                x="Strategy",

                y="Return",

                title="Strategy Returns"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



        # =====================================================
        # TAB 3 - Risk Analytics
        # =====================================================

        with tab3:


            st.subheader(
                "Correlation Matrix"
            )


            correlation = returns_df.corr()



            fig, ax = plt.subplots(

                figsize=(7,5)

            )


            sns.heatmap(

                correlation,

                annot=True,

                cmap="coolwarm",

                ax=ax

            )


            st.pyplot(fig)



            col1, col2 = st.columns(2)



            with col1:


                st.subheader(
                    "Return Contribution"
                )


                rc = return_contribution(
                    returns_df
                )


                st.bar_chart(
                    rc
                )



            with col2:


                st.subheader(
                    "Risk Contribution"
                )


                risk = risk_contribution(
                    returns_df
                )


                st.bar_chart(
                    risk
                )

                
        # =====================================================
        # TAB 4 - Portfolio
        # =====================================================

        with tab4:


            st.subheader(
                "Combined Portfolio"
            )


            st.write(
                "Strategy Allocation"
            )


            weights = (
                returns_df.std()
                /
                returns_df.std().sum()
            )


            st.dataframe(

                weights.rename(
                    "Weight"
                ).to_frame().style.format(
                    "{:.2%}"
                ),

                use_container_width=True

            )



            fig = px.pie(

                values=weights.values,

                names=weights.index,

                title="Portfolio Weights"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



            st.subheader(
                "Portfolio Returns Distribution"
            )


            st.bar_chart(
                combined_returns
            )




        # =====================================================
        # TAB 5 - Walk Forward
        # =====================================================

        with tab5:


            st.subheader(
                "Walk Forward Validation"
            )


            try:


                wf_results = walk_forward_analysis(
                    df
                )


                st.dataframe(

                    wf_results,

                    use_container_width=True

                )


                st.success(
                    "Walk Forward completed successfully"
                )


            except Exception as e:


                st.warning(

                    f"Walk Forward unavailable: {e}"

                )




        # =====================================================
        # TAB 6 - Reports
        # =====================================================

        with tab6:


            st.subheader(
                "Performance Reports"
            )


            report = pd.DataFrame(

                {

                "Metric":

                [

                "Total Return",

                "Annual Return",

                "Volatility",

                "Sharpe Ratio",

                "Sortino Ratio",

                "Calmar Ratio",

                "Maximum Drawdown",

                "Win Rate"

                ],


                "Value":

                [

                total_return,

                annual_return,

                volatility,

                sharpe,

                sortino,

                calmar,

                max_drawdown,

                win_rate

                ]

                }

            )



            st.dataframe(

                report.style.format(

                    {

                    "Value":"{:.4f}"

                    }

                ),

                use_container_width=True

            )



            csv_report = report.to_csv(
                index=False
            )


            st.download_button(

                label="📥 Download Performance Report",

                data=csv_report,

                file_name="performance_report.csv",

                mime="text/csv"

            )



            if "wf_results" in locals():


                csv_wf = wf_results.to_csv(
                    index=False
                )


                st.download_button(

                    label="📥 Download Walk Forward Report",

                    data=csv_wf,

                    file_name="walk_forward_results.csv",

                    mime="text/csv"

                )



else:


    st.info(

        "Select asset and strategies from the sidebar and press Run Analysis."

    )