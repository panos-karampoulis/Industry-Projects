import sys
import os


# ---------------------------------
# Project Root
# ---------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


# ---------------------------------
# External Libraries
# ---------------------------------

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ---------------------------------
# Internal Modules
# ---------------------------------

from app.rag import ask_financial_assistant

# =====================================
# Imports
# =====================================

from app.company import get_company_profile

from app.analysis import (
    generate_company_report
)

from app.market import (
    get_price_history,
    calculate_returns,
    calculate_max_drawdown,
    add_moving_average
)

from app.metrics import (
    calculate_return_statistics
)

from app.comparison import (
    compare_companies,
    build_comparison_context
)


from app.risk_score import (
    generate_company_risk_scores
)


from app.risk_analysis import (
    generate_risk_comparison_report
)

from app.rag import (
    ask_financial_assistant
)



# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide"
)



# =====================================
# Header
# =====================================

st.title(
    "📈 FinSight AI"
)

st.subheader(
    "AI-Powered Financial Research Platform"
)


st.markdown(
    """
    FinSight AI combines financial data,
    quantitative risk analytics and
    local Large Language Models for
    investment research.
    """
)



# =====================================
# Sidebar
# =====================================

st.sidebar.title(
    "⚙️ Research Controls"
)


mode = st.sidebar.radio(
    "Select Analysis",
    [
        "Single Company",
        "Company Comparison",
        "Risk Comparison AI"
    ]
)



companies = [
    "MSFT",
    "NVDA",
    "AAPL",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA"
]



# =====================================
# SINGLE COMPANY MODE
# =====================================

if mode == "Single Company":


    ticker = st.sidebar.selectbox(
        "Select Company",
        companies
    )


    period = st.sidebar.selectbox(
        "Historical Period",
        [
            "1y",
            "3y",
            "5y",
            "10y"
        ],
        index=2
    )


    analyze_button = st.sidebar.button(
        "🚀 Analyze"
    )


    if analyze_button:


        try:


            with st.spinner(
                "Loading financial intelligence..."
            ):


                # Company Data

                profile = get_company_profile(
                    ticker
                )


                report = generate_company_report(
                    profile
                )


                summary = report[
                    "company_summary"
                ]


                valuation = report[
                    "valuation"
                ]


                risk = report[
                    "risk_profile"
                ]



                # Market Data

                prices = get_price_history(
                    ticker,
                    period
                )



                # Fix yfinance multi-index columns

                if isinstance(prices.columns, pd.MultiIndex):

                    prices.columns = prices.columns.get_level_values(0)

                returns = calculate_returns(
                    prices
                )


                prices = add_moving_average(
                    prices,
                    50
                )


                prices = add_moving_average(
                    prices,
                    200
                )


                stats = calculate_return_statistics(
                    returns
                )


                drawdown = calculate_max_drawdown(
                    prices
                )



            # Save in session

            st.session_state["ticker"] = ticker
            st.session_state["summary"] = summary
            st.session_state["valuation"] = valuation
            st.session_state["risk"] = risk
            st.session_state["prices"] = prices
            st.session_state["stats"] = stats
            st.session_state["drawdown"] = drawdown



            st.success(
                f"{ticker} analysis completed"
            )


        except Exception as e:

            st.error(
                str(e)
            )



    # =====================================
    # Display if Data Exists
    # =====================================


    if "summary" in st.session_state:


        summary = st.session_state["summary"]

        valuation = st.session_state["valuation"]

        prices = st.session_state["prices"]

        stats = st.session_state["stats"]

        risk = st.session_state["risk"]

        drawdown = st.session_state["drawdown"]



        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🏢 Overview",
                "📈 Market",
                "⚠️ Risk",
                "🤖 AI Assistant"
            ]
        )



        # =====================================
        # OVERVIEW TAB
        # =====================================


        with tab1:


            st.header(
                summary["Company"]
            )


            c1,c2,c3,c4 = st.columns(4)


            c1.metric(
                "Price",
                f"${summary['Price']}"
            )


            c2.metric(
                "Market Cap",
                summary["Market Cap"]
            )


            c3.metric(
                "Beta",
                summary["Beta"]
            )


            c4.metric(
                "Exchange",
                summary["Exchange"]
            )


            st.divider()


            st.subheader(
                "Company Profile"
            )


            st.write(
                f"""
                **Sector:** {summary['Sector']}

                **Industry:** {summary['Industry']}

                **CEO:** {summary['CEO']}

                **Employees:** {summary['Employees']}
                """
            )


            st.subheader(
                "Valuation Snapshot"
            )


            st.json(
                valuation
            )



        # =====================================
        # MARKET TAB
        # =====================================


        with tab2:


            st.header(
                "Market Performance"
            )
            

            st.write(
                prices.tail()
            )

            st.write(
                prices.columns
            )


            fig = go.Figure()


            fig.add_trace(
                go.Scatter(
                    x=prices.index,
                    y=prices["Close"],
                    name="Price"
                )
            )


            fig.add_trace(
                go.Scatter(
                    x=prices.index,
                    y=prices["MA_50"],
                    name="MA 50"
                )
            )


            fig.add_trace(
                go.Scatter(
                    x=prices.index,
                    y=prices["MA_200"],
                    name="MA 200"
                )
            )


            fig.update_layout(
                height=500,
                template="plotly_white"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


                    # =====================================
        # RISK TAB
        # =====================================

        with tab3:

            st.header(
                "⚠️ Quant Risk Analytics"
            )


            c1, c2, c3 = st.columns(3)


            c1.metric(
                "Annual Return",
                f"{stats['Annual Return']*100:.2f}%"
            )


            c2.metric(
                "Volatility",
                f"{stats['Annual Volatility']*100:.2f}%"
            )


            c3.metric(
                "Sharpe Ratio",
                f"{stats['Sharpe Ratio']:.2f}"
            )


            c4, c5, c6 = st.columns(3)


            c4.metric(
                "Sortino Ratio",
                f"{stats['Sortino Ratio']:.2f}"
            )


            c5.metric(
                "VaR 95%",
                f"{stats['VaR 95%']*100:.2f}%"
            )


            c6.metric(
                "Max Drawdown",
                f"{drawdown*100:.2f}%"
            )


            st.divider()


            st.subheader(
                "Risk Assessment"
            )


            st.warning(
                risk["risk"]
            )


            st.write(
                risk["comment"]
            )



        # =====================================
        # AI ASSISTANT TAB
        # =====================================

        # =====================================
        # AI ASSISTANT TAB
        # =====================================

        with tab4:


            st.header(
                "🤖 FinSight AI Research Assistant"
            )


            st.markdown(
                """
                Ask questions about company annual reports
                and risk disclosures.

                Powered by:
                - FAISS Retrieval
                - Sentence Transformer Embeddings
                - Ollama Llama 3.2 Local LLM
                """
            )


            company = st.selectbox(
                "Select Company",
                [
                    "amazon",
                    "microsoft",
                    "nvidia"
                ],
                format_func=lambda x: x.upper()
            )



            question = st.text_input(
                "Ask a financial question",
                placeholder=
                "What are the main AI risks?"
            )



            if st.button(
                "Generate Answer",
                key="ai_button"
            ):


                if question:


                    try:


                        with st.spinner(
                            "Analyzing documents..."
                        ):


                            response = ask_financial_assistant(
                                question,
                                company
                            )



                        st.subheader(
                            "🤖 AI Analysis"
                        )


                        st.write(
                            response["answer"]
                        )



                        st.divider()



                        st.subheader(
                            "📚 Evidence Retrieved"
                        )



                        for source in response["sources"]:


                            with st.expander(
                                f"{source['company'].upper()} | Chunk {source['source_id']} | Distance: {source['score']}"
                        ):


                                st.write(
                                    source["text"]
                                )



                    except Exception as e:


                        st.error(
                            str(e)
                        )


                else:


                    st.warning(
                        "Please enter a question."
                    )

# =====================================
# COMPANY COMPARISON MODE
# =====================================


else:


    st.sidebar.subheader(
        "Company Comparison"
    )


    selected_companies = st.sidebar.multiselect(
        "Select Companies",
        companies,
        default=[
            "MSFT",
            "NVDA",
            "AAPL"
        ]
    )


    compare_button = st.sidebar.button(
        "Compare"
    )



    if compare_button:


        try:


            with st.spinner(
                "Comparing companies..."
            ):


                df = compare_companies(
                    selected_companies
                )


            st.header(
                "📊 Company Comparison"
            )


            st.dataframe(
                df,
                use_container_width=True
            )


            st.divider()


            st.subheader(
                "Beta Risk Comparison"
            )


            fig = px.bar(
                df,
                x="Symbol",
                y="Beta",
                title=
                "Market Risk Comparison"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )



        except Exception as e:


            st.error(
                str(e)
            )



# =================================
# RISK COMPARISON AI MODE
# =================================


    elif mode == "Risk Comparison AI":


        st.header(
            "⚠️ FinSight AI Risk Comparison"
        )


        st.write(
            """
            Compare risk factors across multiple
            companies using annual report evidence.
            """
        )


        companies = st.multiselect(
            "Select Companies",
            [
                "amazon",
                "microsoft",
                "nvidia"
            ],
            default=[
                "amazon",
                "microsoft",
                "nvidia"
            ]
        )


        question = st.text_input(
            "Risk Question",
            value=
            "Compare AI risks between these companies"
        )



        if st.button(
            "Generate Risk Comparison"
        ):


            if companies:


                with st.spinner(
                    "Analyzing company risks..."
                ):


                    context, sources = build_comparison_context(
                        companies,
                        question,
                        top_k=5
                    )


                    report = generate_risk_comparison_report(
                        question,
                        context
                    )

                    risk_scores = generate_company_risk_scores(
                        sources
                    )



                st.subheader(
                    "AI Risk Comparison Report"
                )


                st.markdown(
                    report
                )


                st.subheader(
                     "📊 AI Risk Scores"
                )


                for item in risk_scores:


                    st.metric(
                        item["Company"],
                        f"{item['AI Risk Score']}/10"
                    )



                st.subheader(
                    "Evidence Sources"
                )


                for source in sources:


                    with st.expander(
                        f"{source['company'].upper()} | Chunk {source['source_id']} | Distance {source['score']}"
                    ):

                        st.write(
                            source["text"]
                        )

            else:

                st.warning(
                    "Select at least one company."
                )



# =====================================
# Footer
# =====================================


st.sidebar.divider()


st.sidebar.caption(
    """
    FinSight AI v1.1

    AI Financial Research Platform

    Python | Streamlit | FAISS | Ollama
    """
)