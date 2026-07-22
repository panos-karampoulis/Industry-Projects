import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path
from io import BytesIO

from analyst import generate_llm_analysis

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet



# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Investment Decision Engine",
    page_icon="📈",
    layout="wide"
)



# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)



# =====================================================
# LOAD DATA
# =====================================================

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


    company_financials = pd.read_csv(
        DATA_DIR / "company_financials.csv"
    )


    return (
        metrics,
        equity,
        ml_signals,
        feature_importance,
        shap_values,
        company_financials
    )



(
    metrics,
    equity,
    ml_signals,
    feature_importance,
    shap_values,
    company_financials

) = load_data()



# =====================================================
# AI ANALYST FALLBACK SUMMARY
# =====================================================

def generate_analyst_summary(
        company,
        signal,
        probability
):


    name = company.get(
        "companyName",
        company.get(
            "symbol",
            "Company"
        )
    )


    positives = []


    risks = []



    if company.get(
        "operatingMargin",
        0
    ) > 0.30:

        positives.append(
            "exceptional operating profitability"
        )


    elif company.get(
        "operatingMargin",
        0
    ) > 0.15:

        positives.append(
            "healthy operating margins"
        )



    if company.get(
        "netMargin",
        0
    ) > 0.15:

        positives.append(
            "strong net profitability"
        )



    if company.get(
        "freeCashFlowQuality",
        0
    ) > 0.5:

        positives.append(
            "strong free cash flow generation"
        )



    if company.get(
        "peRatio",
        0
    ) > 40:

        risks.append(
            "elevated valuation multiples"
        )



    if company.get(
        "beta",
        1
    ) > 1.5:

        risks.append(
            "high market sensitivity"
        )



    if not positives:

        positives.append(
            "mixed fundamental profile"
        )



    if not risks:

        risks.append(
            "no major quantitative risks detected"
        )



    return f"""

AI Equity Research Summary


{name} receives a {signal} rating.


Model confidence:

{probability:.1%}


Investment Thesis:

The model identifies {", ".join(positives)}
as the primary investment drivers.


Risk Factors:

{", ".join(risks)}


Conclusion:

The investment view combines financial quality,
machine learning prediction and explainable AI.

"""

# =====================================================
# DASHBOARD COMPONENTS
# =====================================================


def metric_card(
        title,
        value,
        color="#16a34a",
        icon="📊"
):

    st.markdown(
        f"""
        <div style="
            background:white;
            border-radius:14px;
            padding:18px;
            border-left:8px solid {color};
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

        <div style="
            font-size:15px;
            color:#666;
        ">
            {icon} {title}
        </div>

        <div style="
            font-size:32px;
            font-weight:bold;
            color:{color};
            margin-top:10px;
        ">
            {value}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )




def probability_gauge(probability):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=probability * 100,

            title={
                "text":"AI Confidence"
            },


            gauge={

                "axis":{
                    "range":[0,100]
                },


                "bar":{
                    "color":"#16a34a"
                },


                "steps":[

                    {
                        "range":[0,40],
                        "color":"#fee2e2"
                    },

                    {
                        "range":[40,70],
                        "color":"#fef3c7"
                    },

                    {
                        "range":[70,100],
                        "color":"#dcfce7"
                    }

                ]
            }
        )
    )


    fig.update_layout(
        height=280,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )


    return fig





def score_gauge(
        score,
        title
):

    if score >= 75:

        color="#16a34a"


    elif score >=50:

        color="#f59e0b"


    else:

        color="#dc2626"



    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,


            title={
                "text":title
            },


            gauge={

                "axis":{
                    "range":[0,100]
                },


                "bar":{
                    "color":color
                },


                "steps":[

                    {
                        "range":[0,50],
                        "color":"#fee2e2"
                    },

                    {
                        "range":[50,75],
                        "color":"#fef3c7"
                    },

                    {
                        "range":[75,100],
                        "color":"#dcfce7"
                    }

                ]
            }
        )
    )


    fig.update_layout(
        height=250,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )


    return fig





# =====================================================
# INVESTMENT SCORING ENGINE
# =====================================================


def calculate_quality_score(company):

    score = 50


    if company.get(
        "operatingMargin",
        0
    ) > 0.20:

        score += 15



    if company.get(
        "netMargin",
        0
    ) > 0.15:

        score += 15



    if company.get(
        "freeCashFlowQuality",
        0
    ) > 0.5:

        score += 15



    if company.get(
        "currentRatio",
        0
    ) > 1.5:

        score += 5



    return min(
        score,
        100
    )




def calculate_risk_score(company):

    score = 50


    beta = company.get(
        "beta",
        1
    )


    if beta < 1:

        score +=15


    elif beta >1.5:

        score -=15



    debt = company.get(
        "debtEquity",
        0
    )


    if debt <0.5:

        score +=15


    elif debt >2:

        score -=20



    if company.get(
        "currentRatio",
        1
    ) <1:

        score -=15



    return max(
        min(score,100),
        0
    )




def calculate_valuation_score(company):

    score = 50


    pe = company.get(
        "peRatio",
        0
    )


    if pe <20:

        score +=20


    elif pe >40:

        score -=20



    peg = company.get(
        "pegRatio",
        0
    )


    if peg >0 and peg <1:

        score +=20



    pb = company.get(
        "pbRatio",
        0
    )


    if pb <5:

        score +=10



    return max(
        min(score,100),
        0
    )


# =====================================================
# SHAP ANALYSIS HELPERS
# =====================================================


def get_shap_drivers(
        shap_data,
        top_n=5
):


    sorted_shap = (
        shap_data
        .sort_values(
            "SHAP",
            ascending=False
        )
    )


    positive = sorted_shap.head(
        top_n
    )


    negative = (
        sorted_shap
        .tail(top_n)
        .sort_values(
            "SHAP"
        )
    )


    return (
        positive,
        negative
    )




def generate_risk_factors(company):


    risks = []



    if company.get(
        "peRatio",
        0
    ) > 40:

        risks.append(
            "High valuation multiples"
        )



    if company.get(
        "beta",
        1
    ) > 1.5:

        risks.append(
            "High market volatility exposure"
        )



    if company.get(
        "debtEquity",
        0
    ) > 2:

        risks.append(
            "Elevated leverage"
        )



    if not risks:

        risks.append(
            "No major quantitative risks detected"
        )


    return risks





# =====================================================
# PROFESSIONAL PDF REPORT
# =====================================================


def create_pdf_report(
        company,
        signal,
        probability,
        shap_data,
        quality,
        risk,
        valuation,
        ai_summary
):


    buffer = BytesIO()


    doc = SimpleDocTemplate(
        buffer
    )


    styles = getSampleStyleSheet()


    story = []



    # TITLE

    story.append(
        Paragraph(
            "AI Investment Research Report",
            styles["Title"]
        )
    )


    story.append(
        Spacer(
            1,
            25
        )
    )



    # COMPANY OVERVIEW

    story.append(
        Paragraph(
            "Company Overview",
            styles["Heading2"]
        )
    )


    company_text = f"""

    Company: {company.get('companyName','')}<br/>

    Symbol: {company.get('symbol','')}<br/>

    Sector: {company.get('sector','')}<br/>

    Industry: {company.get('industry','')}<br/>

    Market Cap: {company.get('marketCap','')}

    """


    story.append(
        Paragraph(
            company_text,
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # AI PREDICTION


    story.append(
        Paragraph(
            "AI Model Prediction",
            styles["Heading2"]
        )
    )


    prediction = f"""

    Signal: {signal}<br/>

    Confidence: {probability:.2%}<br/>

    Quality Score: {quality}/100<br/>

    Risk Score: {risk}/100<br/>

    Valuation Score: {valuation}/100

    """


    story.append(
        Paragraph(
            prediction,
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # INVESTMENT THESIS


    story.append(
        Paragraph(
            "Investment Thesis",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            ai_summary.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # FINANCIAL QUALITY


    story.append(
        Paragraph(
            "Financial Quality",
            styles["Heading2"]
        )
    )


    metrics_text = ""


    for metric in [

        "grossMargin",
        "operatingMargin",
        "netMargin",
        "currentRatio",
        "quickRatio",
        "peRatio"

    ]:


        if metric in company.index:


            metrics_text += (
                f"{metric}: {company[metric]}<br/>"
            )



    story.append(
        Paragraph(
            metrics_text,
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # RISK FACTORS


    story.append(
        Paragraph(
            "Risk Factors",
            styles["Heading2"]
        )
    )


    risk_text = ""


    for item in generate_risk_factors(company):

        risk_text += (
            f"• {item}<br/>"
        )


    story.append(
        Paragraph(
            risk_text,
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # SHAP DRIVERS


    story.append(
        Paragraph(
            "Explainable AI Drivers",
            styles["Heading2"]
        )
    )


    shap_text = ""


    for idx,row in shap_data.iterrows():


        shap_text += (
            f"{idx}: {row['SHAP']:.4f}<br/>"
        )


    story.append(
        Paragraph(
            shap_text,
            styles["BodyText"]
        )
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # CONCLUSION


    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            """
            The investment decision combines machine learning,
            fundamental analysis and explainable AI to provide
            a structured equity research view.
            """,
            styles["BodyText"]
        )
    )



    doc.build(
        story
    )


    buffer.seek(0)


    return buffer


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================


st.sidebar.title(
    "AI Investment Engine"
)


page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Portfolio",
        "🤖 ML Signals",
        "🧠 Explainability",
        "🔍 Stock Analysis",
        "📈 Backtest",
        "ℹ️ About"
    ]
)



# =====================================================
# HEADER
# =====================================================


st.title(
    "AI Investment Decision Engine"
)


st.caption(
    "Machine Learning powered equity selection & portfolio analytics"
)





# =====================================================
# PORTFOLIO PAGE
# =====================================================


if page == "📊 Portfolio":


    st.subheader(
        "AI Portfolio KPIs"
    )


    ai = metrics.loc[
        "AI Portfolio"
    ]



    c1,c2,c3,c4 = st.columns(4)



    with c1:

        metric_card(
            "Annual Return",
            f"{ai['Annual Return']:.2%}",
            "#16a34a",
            "📈"
        )


    with c2:

        metric_card(
            "Sharpe Ratio",
            f"{ai['Sharpe Ratio']:.2f}",
            "#2563eb",
            "⭐"
        )


    with c3:

        metric_card(
            "Volatility",
            f"{ai['Annual Volatility']:.2%}",
            "#f59e0b",
            "📊"
        )


    with c4:

        metric_card(
            "Maximum Drawdown",
            f"{ai['Maximum Drawdown']:.2%}",
            "#dc2626",
            "⚠️"
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





# =====================================================
# BACKTEST PAGE
# =====================================================


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

        template="plotly_white",

        yaxis_title="Growth"

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

        template="plotly_white",

        yaxis_title="Drawdown"

    )



    st.plotly_chart(
        fig2,
        use_container_width=True
    )





# =====================================================
# ML SIGNALS PAGE
# =====================================================


elif page == "🤖 ML Signals":


    st.subheader(
        "Machine Learning Signals"
    )



    display = ml_signals.copy()



    display["ML_Probability"] = (

        display["ML_Probability"]

        .apply(
            lambda x: f"{x:.1%}"
        )

    )



    st.dataframe(
        display,
        use_container_width=True
    )





# =====================================================
# EXPLAINABILITY PAGE
# =====================================================


elif page == "🧠 Explainability":


    st.subheader(
        "Feature Importance"
    )



    fi = feature_importance.copy()



    st.bar_chart(

        fi.set_index(

            fi.columns[0]

        )

    )



    st.divider()



    st.subheader(
        "SHAP Explanation"
    )



    stock = st.selectbox(

        "Select Stock",

        shap_values["symbol"].unique()

    )



    stock_shap = shap_values[

        shap_values["symbol"] == stock

    ]



    stock_shap = (

        stock_shap

        .drop(
            columns=["symbol"]
        )

        .T

    )


    stock_shap.columns = [

        "SHAP"

    ]



    stock_shap = (

        stock_shap

        .sort_values(
            "SHAP"
        )

    )



    st.bar_chart(
        stock_shap
    )


# =====================================================
# STOCK ANALYSIS PAGE
# =====================================================


elif page == "🔍 Stock Analysis":


    st.subheader(
        "🔍 Stock Analysis"
    )



    stock = st.selectbox(

        "Select Stock",

        company_financials["symbol"].unique()

    )



    company = company_financials[

        company_financials["symbol"] == stock

    ].iloc[0]



    st.header(
        company["companyName"]
    )



    # -------------------------
    # SCORES
    # -------------------------

    quality = calculate_quality_score(
        company
    )


    risk = calculate_risk_score(
        company
    )


    valuation = calculate_valuation_score(
        company
    )



    signal_row = ml_signals[

        ml_signals["symbol"] == stock

    ].iloc[0]



    signal = signal_row["Signal"]

    probability = signal_row["ML_Probability"]



    # -------------------------
    # KPI CARDS
    # -------------------------


    st.subheader(
        "📊 Investment Dashboard"
    )


    if signal == "BUY":

        signal_color="#16a34a"
        signal_icon="🟢"


    elif signal == "SELL":

        signal_color="#dc2626"
        signal_icon="🔴"


    else:

        signal_color="#f59e0b"
        signal_icon="🟡"




    k1,k2,k3,k4,k5 = st.columns(5)



    with k1:

        metric_card(

            "AI Signal",

            f"{signal_icon} {signal}",

            signal_color,

            "🤖"

        )



    with k2:

        metric_card(

            "Confidence",

            f"{probability:.1%}",

            "#2563eb",

            "🎯"

        )



    with k3:

        metric_card(

            "Quality",

            f"{quality}/100",

            "#16a34a",

            "⭐"

        )



    with k4:

        metric_card(

            "Risk",

            f"{risk}/100",

            "#f59e0b",

            "⚠️"

        )



    with k5:

        metric_card(

            "Valuation",

            f"{valuation}/100",

            "#7c3aed",

            "💰"

        )



    st.divider()



    # -------------------------
    # CONFIDENCE GAUGE
    # -------------------------


    st.plotly_chart(

        probability_gauge(
            probability
        ),

        use_container_width=True

    )



    st.divider()



    # -------------------------
    # SCORE GAUGES
    # -------------------------


    g1,g2,g3 = st.columns(3)



    with g1:

        st.plotly_chart(

            score_gauge(
                quality,
                "⭐ Quality Score"
            ),

            use_container_width=True

        )



    with g2:

        st.plotly_chart(

            score_gauge(
                risk,
                "⚠ Risk Score"
            ),

            use_container_width=True

        )



    with g3:

        st.plotly_chart(

            score_gauge(
                valuation,
                "💰 Valuation Score"
            ),

            use_container_width=True

        )



    st.divider()



    # -------------------------
    # AI ANALYST
    # -------------------------


    st.subheader(
        "🧠 AI Analyst Summary"
    )



    fallback_summary = generate_analyst_summary(

        company,

        signal,

        probability

    )



    ai_summary = generate_llm_analysis(

        company_name=company["companyName"],

        signal=signal,

        probability=probability,

        quality_score=quality,

        risk_score=risk,

        valuation_score=valuation,

        fallback_summary=fallback_summary

    )



    st.info(
        ai_summary
    )



    st.divider()



    # -------------------------
    # SHAP DRIVERS
    # -------------------------


    st.subheader(
        "📊 Explainable AI Drivers"
    )



    shap_stock = shap_values[

        shap_values["symbol"] == stock

    ]



    if shap_stock.empty:


        st.warning(
            "SHAP explanation unavailable."
        )


    else:


        shap_stock = (

            shap_stock

            .drop(
                columns=["symbol"]
            )

            .T

        )


        shap_stock.columns = [

            "SHAP"

        ]



        positive, negative = get_shap_drivers(

            shap_stock

        )



        c1,c2 = st.columns(2)



        with c1:

            st.success(
                "🟢 Positive Drivers"
            )

            st.dataframe(
                positive
            )



        with c2:

            st.error(
                "🔴 Risk Drivers"
            )

            st.dataframe(
                negative
            )



        st.divider()



        # -------------------------
        # PDF REPORT
        # -------------------------



        pdf = create_pdf_report(

            company,

            signal,

            probability,

            shap_stock,

            quality,

            risk,

            valuation,

            ai_summary

        )



        st.download_button(

            label="📄 Generate AI Research Report",

            data=pdf,

            file_name=f"{stock}_AI_Research_Report.pdf",

            mime="application/pdf"

        )





# =====================================================
# ABOUT PAGE
# =====================================================


elif page == "ℹ️ About":


    st.subheader(
        "AI Investment Decision Engine"
    )


    st.write(
        """
        Machine learning powered equity research platform.

        Features:

        • ML stock classification

        • Explainable AI with SHAP

        • Financial quality scoring

        • Risk analytics

        • AI generated investment reports

        """
    )