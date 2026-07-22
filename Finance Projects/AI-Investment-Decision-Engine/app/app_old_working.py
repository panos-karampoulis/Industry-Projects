import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
from analyst import generate_llm_analysis
from report_generator import create_research_report

from pathlib import Path
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="AI Investment Decision Engine",
    page_icon="📈",
    layout="wide"
)


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)



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



# =========================
# AI ANALYST SUMMARY
# =========================

def generate_analyst_summary(
        company,
        signal,
        probability
):

    name = company.get(
        "companyName",
        company.get("symbol", "Company")
    )


    quality_points = []
    risk_points = []


    operating_margin = company.get(
        "operatingMargin",
        0
    )


    net_margin = company.get(
        "netMargin",
        0
    )


    fcf_quality = company.get(
        "freeCashFlowQuality",
        0
    )


    pe_ratio = company.get(
        "peRatio",
        0
    )


    # Quality analysis

    if operating_margin > 0.30:

        quality_points.append(
            "exceptional operating profitability"
        )

    elif operating_margin > 0.15:

        quality_points.append(
            "healthy operating margins"
        )


    if net_margin > 0.15:

        quality_points.append(
            "strong net profitability"
        )


    if fcf_quality > 0.5:

        quality_points.append(
            "strong free cash flow quality"
        )


    # Risk analysis

    if pe_ratio > 40:

        risk_points.append(
            "elevated valuation multiples"
        )


    if company.get("beta",1) > 1.5:

        risk_points.append(
            "higher market sensitivity"
        )


    quality_text = ", ".join(
        quality_points
    )


    risk_text = ", ".join(
        risk_points
    )


    if not quality_text:

        quality_text = (
            "mixed financial characteristics"
        )


    if not risk_text:

        risk_text = (
            "no major quantitative risks detected"
        )


    summary = f"""

## AI Equity Research Summary


**{name} receives a {signal} recommendation.**

Model confidence:

**{probability:.1%}**


### Investment Thesis

The model identifies {quality_text}
as the primary drivers behind the investment decision.


### Key Risks

The main risk factors include:

{risk_text}


### Analyst Conclusion

The recommendation combines financial
fundamentals, machine learning prediction
and explainable AI analysis.

"""


    return summary


def metric_card(
    title,
    value,
    color="#16a34a",
    icon="📊"
):

    st.markdown(
        f"""
        <div style="
            background-color:#ffffff;
            border-radius:14px;
            padding:18px;
            border-left:8px solid {color};
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

        <div style="
            font-size:16px;
            color:#666;
        ">
            {icon} {title}
        </div>

        <div style="
            font-size:34px;
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
                "text": "AI Confidence"
            },
            gauge={
                "axis": {
                    "range": [0,100]
                },
                "bar": {
                    "color": "#16a34a"
                },
                "steps": [
                    {
                        "range": [0,40],
                        "color": "#fee2e2"
                    },
                    {
                        "range": [40,70],
                        "color": "#fef3c7"
                    },
                    {
                        "range": [70,100],
                        "color": "#dcfce7"
                    }
                ]
            }
        )
    )


    fig.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )


    return fig


def score_gauge(score, title):

    if score >= 75:
        color = "#16a34a"

    elif score >= 50:
        color = "#f59e0b"

    else:
        color = "#dc2626"


    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={
                "text": title
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
        margin={
            "l":20,
            "r":20,
            "t":50,
            "b":20
        }
    )


    return fig





def calculate_quality_score(company):

    score = 50

    if company.get("operatingMargin",0) > 0.20:
        score += 15

    if company.get("netMargin",0) > 0.15:
        score += 15

    if company.get("freeCashFlowQuality",0) > 0.5:
        score += 15

    if company.get("currentRatio",0) > 1.5:
        score += 5

    return min(score,100)



def calculate_risk_score(company):

    score = 50

    beta = company.get("beta",1)

    if beta < 1:
        score += 15

    elif beta > 1.5:
        score -= 15


    debt = company.get("debtEquity",0)

    if debt < 0.5:
        score += 15

    elif debt > 2:
        score -= 20


    if company.get("currentRatio",1) < 1:
        score -= 15


    return max(min(score,100),0)



def calculate_valuation_score(company):

    score = 50

    pe = company.get("peRatio",0)

    if pe < 20:
        score += 20

    elif pe > 40:
        score -= 20


    peg = company.get("pegRatio",0)

    if peg > 0 and peg < 1:
        score += 20


    pb = company.get("pbRatio",0)

    if pb < 5:
        score += 10


    return max(min(score,100),0)





# =========================
# PDF REPORT
# =========================

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


    story.append(
        Paragraph(
            "AI Investment Decision Report",
            styles["Title"]
        )
    )


    story.append(
        Spacer(1,20)
    )



    story.append(
        Paragraph(
            f"""
            Company: {company['companyName']}<br/>
            Symbol: {company['symbol']}<br/>
            Sector: {company['sector']}<br/>
            Industry: {company['industry']}<br/><br/>

            AI Signal: {signal}<br/>
            ML Probability: {probability:.2%}
            """,
            styles["BodyText"]
        )
    )


    story.append(
        Spacer(1,20)
    )


    story.append(
        Paragraph(
            "AI Analyst Summary",
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
        Spacer(1,20)
    )


    story.append(
        Paragraph(
            "Financial Metrics",
            styles["Heading2"]
        )
    )


    metrics_text = ""


    for col in [
        "grossMargin",
        "operatingMargin",
        "netMargin",
        "peRatio",
        "currentRatio",
        "quickRatio"
    ]:

        if col in company.index:

            metrics_text += (
                f"{col}: {company[col]}<br/>"
            )


    story.append(
        Paragraph(
            metrics_text,
            styles["BodyText"]
        )
    )


    # =========================
    # Investment Scores
    # =========================

    story.append(
        Spacer(1,20)
    )


    story.append(
        Paragraph(
            "Investment Scores",
            styles["Heading2"]
        )
    )


    scores_text = f"""

    Quality Score: {quality}/100<br/>

    Risk Score: {risk}/100<br/>

    Valuation Score: {valuation}/100

    """


    story.append(
        Paragraph(
            scores_text,
            styles["BodyText"]
        )
    )


    # =========================
    # SHAP Drivers
    # =========================

    story.append(
        Spacer(1,20)
    )


    story.append(
        Paragraph(
            "SHAP Drivers",
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


    doc.build(
        story
    )


    buffer.seek(0)

    return buffer




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
        "🔍 Stock Analysis",
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
        "Max Drawdown",
        f"{ai['Maximum Drawdown']:.2%}",
        "#dc2626",
        "⚠"
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
        template="plotly_white",
        yaxis_title="Growth of $1"
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

# =========================
# ML SIGNALS
# =========================

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



# =========================
# EXPLAINABILITY
# =========================

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




# =========================
# STOCK ANALYSIS
# =========================

elif page == "🔍 Stock Analysis":


    st.subheader(
        "Stock Analysis"
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


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Sector",
        company["sector"]
    )


    c2.metric(
        "Industry",
        company["industry"]
    )


    c3.metric(
        "Market Cap",
        f"${company['marketCap']/1e12:.2f}T"
    )


    c4.metric(
        "Price",
        f"${company['price']:.2f}"
    )


    st.divider()



    st.subheader(
        "Financial Quality"
    )


    financial_cols = [
        "grossMargin",
        "operatingMargin",
        "netMargin",
        "currentRatio",
        "quickRatio"
    ]


    cols = st.columns(
        len(financial_cols)
    )


    for col,metric in zip(
        cols,
        financial_cols
    ):

        if metric in company.index:

            value = company[metric]


            if "Margin" in metric:

                value = f"{value:.2%}"

            else:

                value = f"{value:.2f}"


            col.metric(
                metric,
                value
            )



    st.divider()



    st.subheader(
        "AI Decision"
    )


    signal_row = ml_signals[
        ml_signals["symbol"] == stock
    ].iloc[0]


    st.metric(
        "Signal",
        signal_row["Signal"]
    )


    st.subheader(
        "Model Confidence"
    )


    st.plotly_chart(
        probability_gauge(
            signal_row["ML_Probability"]
        ),
        use_container_width=True
    )




    st.divider()

    st.subheader(
        "Investment Scores"
    )


    quality = calculate_quality_score(
        company
    )

    risk = calculate_risk_score(
        company
    )

    valuation = calculate_valuation_score(
        company
    )


    cc1,c2,c3 = st.columns(3)


    with c1:

        st.plotly_chart(
            score_gauge(
                quality,
                "⭐ Quality Score"
            ),
            use_container_width=True
        )


    with c2:

        st.plotly_chart(
            score_gauge(
                risk,
                "⚠ Risk Score"
            ),
            use_container_width=True
        )


    with c3:

        st.plotly_chart(
            score_gauge(
                valuation,
                "💰 Valuation Score"
            ),
            use_container_width=True
        )


    st.divider()


    st.subheader(
        "AI Analyst Summary"
    )


    fallback_summary = generate_analyst_summary(
        company,
        signal_row["Signal"],
        signal_row["ML_Probability"]
    )


    ai_summary = generate_llm_analysis(
        company_name=company["companyName"],
        signal=signal_row["Signal"],
        probability=signal_row["ML_Probability"],
        quality_score=quality,
        risk_score=risk,
        valuation_score=valuation,
        fallback_summary=fallback_summary
    )


    st.info(
        ai_summary
    )
    


   

    st.divider()


    st.subheader(
        "SHAP Drivers"
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


        shap_stock = (
            shap_stock
            .sort_values(
                "SHAP"
            )
        )


        st.bar_chart(
            shap_stock
        )



        pdf = create_pdf_report(
            company,
            signal_row["Signal"],
            signal_row["ML_Probability"],
            shap_stock,
            quality,
            risk,
            valuation,
            ai_summary
        )


        st.download_button(
            label="📄 Generate AI Report",
            data=pdf,
            file_name=f"{stock}_AI_Report.pdf",
            mime="application/pdf"
        )





# =========================
# ABOUT
# =========================

elif page == "ℹ️ About":


    st.subheader(
        "AI Investment Decision Engine"
    )


    st.write(
        """
        Machine learning based investment research platform.

        Features:
        - Portfolio optimization
        - ML stock classification
        - Explainable AI with SHAP
        - Risk analytics
        - Automated investment reports
        """
    )