import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]


DEMO_DIR = PROJECT_ROOT / "demo_data"

RESULTS_DIR = DEMO_DIR / "results"

FEATURE_IMPORTANCE_DIR = DEMO_DIR / "feature_importance"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="Model Comparison",

    page_icon="📊",

    layout="wide"

)



# ============================================================
# TITLE
# ============================================================


st.title(

    "📊 Machine Learning Model Comparison"

)


st.markdown(

"""
Comparison of electricity price forecasting models.
"""

)



# ============================================================
# LOAD RESULTS
# ============================================================


@st.cache_data
def load_results(country):


    models = [

        "random_forest",

        "xgboost",

        "lightgbm",

        

    ]


    results = []



    for model in models:


        file = (

            RESULTS_DIR
            /
            country
            /
            f"{model}_results.csv"

        )


        if file.exists():


            df = pd.read_csv(
                file
            )


            # ensure country column exists

            if "country" not in df.columns:

                df["country"] = country



            df["model"] = model



            results.append(df)



    if len(results) == 0:

        return None



    final = pd.concat(

        results,

        ignore_index=True

    )


    return final





# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.header(

    "⚙️ Comparison Settings"

)



country = st.sidebar.selectbox(

    "Country",

    [

        "germany",

        "greece"

    ]

)



results = load_results(

    country

)



if results is None:


    st.error(

        "No results files found"

    )


    st.stop()



st.sidebar.success(

    f"{country.upper()} loaded"

)

# ============================================================
# RESULTS TABLE
# ============================================================


st.subheader(

    "📋 Model Performance"

)



# sort columns

results_display = results.copy()

results_display = results_display[
    [
        "model",
        "country",
        "MAE",
        "RMSE"
    ]
]



# format model names

results_display["model"] = (

    results_display["model"]

    .str.replace("_", " ")

    .str.title()

)



st.dataframe(

    results_display,

    use_container_width=True

)





# ============================================================
# MAE COMPARISON
# ============================================================


st.subheader(

    "📉 Mean Absolute Error (MAE)"

)



fig_mae = px.bar(

    results_display,

    x="model",

    y="MAE",

    text="MAE",

    title=(

        f"{country.upper()} - MAE Comparison"

    )

)



fig_mae.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)



fig_mae.update_layout(

    height=450,

    xaxis_title="Model",

    yaxis_title="MAE €/MWh"

)



st.plotly_chart(

    fig_mae,

    use_container_width=True

)





# ============================================================
# RMSE COMPARISON
# ============================================================


st.subheader(

    "📈 Root Mean Squared Error (RMSE)"

)



fig_rmse = px.bar(

    results_display,

    x="model",

    y="RMSE",

    text="RMSE",

    title=(

        f"{country.upper()} - RMSE Comparison"

    )

)



fig_rmse.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)



fig_rmse.update_layout(

    height=450,

    xaxis_title="Model",

    yaxis_title="RMSE €/MWh"

)



st.plotly_chart(

    fig_rmse,

    use_container_width=True

)

# ============================================================
# FEATURE IMPORTANCE EXPLORER
# ============================================================


st.subheader(

    "🔍 Feature Importance Explorer"

)



model_mapping = {

    "Random Forest": "random_forest",

    "XGBoost": "xgboost",

    "LightGBM": "lightgbm",

   

}



model_display = st.selectbox(

    "Select Model",

    list(model_mapping.keys())

)



model_choice = model_mapping[model_display]



importance_file = (

    FEATURE_IMPORTANCE_DIR
    /
    f"{model_choice}_feature_importance.csv"

)


if importance_file.exists():


    importance = pd.read_csv(

        importance_file

    )


    # sort

    importance = importance.sort_values(

        by="importance",

        ascending=False

    )



    top_features = importance.head(10)



    fig_features = px.bar(

        top_features.sort_values(

            "importance"

        ),

        x="importance",

        y="feature",

        orientation="h",

        title=(

            f"{model_choice.title()} - Top 10 Features"

        )

    )



    fig_features.update_layout(

        height=500,

        xaxis_title="Importance",

        yaxis_title="Feature"

    )



    st.plotly_chart(

        fig_features,

        use_container_width=True

    )



    st.dataframe(

        top_features,

        use_container_width=True

    )


else:


    st.info(

        "Feature importance file not available"

    )





# ============================================================
# BEST MODEL
# ============================================================


st.subheader(

    "🏆 Best Forecasting Model"

)



best_model = (

    results_display

    .sort_values(

        by="MAE",

        ascending=True

    )

    .iloc[0]

)



col1, col2, col3 = st.columns(3)


col1.metric(

    "🏆 Best Model",

    str(best_model["model"])

)


col2.metric(

    "📉 MAE",

    f"{float(best_model['MAE']):.2f} €/MWh"

)


col3.metric(

    "📈 RMSE",

    f"{float(best_model['RMSE']):.2f} €/MWh"

)



st.success(
    f"""
For **{country.upper()}**, the best performing model is:

### 🏆 {best_model['model'].replace("_"," ").title()}

Performance:

- **MAE:** {best_model['MAE']:.2f} €/MWh
- **RMSE:** {best_model['RMSE']:.2f} €/MWh

"""
)