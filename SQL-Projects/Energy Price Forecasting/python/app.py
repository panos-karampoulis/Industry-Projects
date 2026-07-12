import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Energy Price Forecasting",
    layout="wide"
)


# =========================
# Title
# =========================

st.title("⚡ Energy Price Forecasting Dashboard")

st.write(
    "Machine Learning dashboard for electricity market price forecasting"
)


# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "energy_market_prices.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "energy_price_model.pkl"
)


# =========================
# Load Data
# =========================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    return df


df = load_data()


# =========================
# Load Model
# =========================

@st.cache_resource
def load_model():

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        return pickle.load(file)


model = load_model()



# =========================
# Sidebar Inputs
# =========================

st.sidebar.header(
    "⚡ Forecast Controls"
)


demand = st.sidebar.slider(
    "Demand (MWh)",
    int(df.Demand_MWh.min()),
    int(df.Demand_MWh.max()),
    int(df.Demand_MWh.mean())
)


wind = st.sidebar.slider(
    "Wind Generation (MWh)",
    int(df.Wind_Generation_MWh.min()),
    int(df.Wind_Generation_MWh.max()),
    int(df.Wind_Generation_MWh.mean())
)


solar = st.sidebar.slider(
    "Solar Generation (MWh)",
    int(df.Solar_Generation_MWh.min()),
    int(df.Solar_Generation_MWh.max()),
    int(df.Solar_Generation_MWh.mean())
)


gas = st.sidebar.slider(
    "Gas Price €/MWh",
    float(df.Gas_Price_EUR.min()),
    float(df.Gas_Price_EUR.max()),
    float(df.Gas_Price_EUR.mean())
)


co2 = st.sidebar.slider(
    "CO2 Price €/ton",
    float(df.CO2_Price_EUR.min()),
    float(df.CO2_Price_EUR.max()),
    float(df.CO2_Price_EUR.mean())
)


temperature = st.sidebar.slider(
    "Temperature °C",
    float(df.Temperature_C.min()),
    float(df.Temperature_C.max()),
    float(df.Temperature_C.mean())
)



# =========================
# KPI Section
# =========================

st.subheader("📊 Market Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Average Price",
        f"{df.Electricity_Price_EUR.mean():.2f} €/MWh"
    )


with col2:
    st.metric(
        "Maximum Price",
        f"{df.Electricity_Price_EUR.max():.2f} €/MWh"
    )


with col3:
    st.metric(
        "Minimum Price",
        f"{df.Electricity_Price_EUR.min():.2f} €/MWh"
    )


with col4:
    st.metric(
        "Average Demand",
        f"{df.Demand_MWh.mean():,.0f} MWh"
    )



# =========================
# Tabs
# =========================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Market Analysis",
        "🤖 Prediction",
        "🧠 Model Performance",
        "ℹ️ Data"
    ]
)



# =========================
# Market Analysis
# =========================

with tab1:

    st.subheader(
        "Electricity Price Trend"
    )


    fig1 = px.line(
        df,
        x="Date",
        y="Electricity_Price_EUR",
        title="Electricity Market Price"
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )



    st.subheader(
        "Demand vs Electricity Price"
    )


    fig2 = px.scatter(
        df,
        x="Demand_MWh",
        y="Electricity_Price_EUR",
        title="Demand Impact on Price"
    )


    st.plotly_chart(
        fig2,
        width="stretch"
    )



    st.subheader(
        "Renewable Generation"
    )


    renewable = df[
        [
            "Date",
            "Wind_Generation_MWh",
            "Solar_Generation_MWh"
        ]
    ]


    renewable = renewable.melt(
        id_vars="Date",
        var_name="Source",
        value_name="Generation"
    )


    fig3 = px.line(
        renewable,
        x="Date",
        y="Generation",
        color="Source",
        title="Renewable Energy Production"
    )


    st.plotly_chart(
        fig3,
        width="stretch"
    )



    st.subheader(
        "Gas and CO2 Prices"
    )


    prices = df[
        [
            "Date",
            "Gas_Price_EUR",
            "CO2_Price_EUR"
        ]
    ]


    prices = prices.melt(
        id_vars="Date",
        var_name="Factor",
        value_name="Price"
    )


    fig4 = px.line(
        prices,
        x="Date",
        y="Price",
        color="Factor",
        title="Fuel Cost Drivers"
    )


    st.plotly_chart(
        fig4,
        width="stretch"
    )



# =========================
# Prediction
# =========================

with tab2:

    st.subheader(
        "Electricity Price Prediction"
    )


    input_data = pd.DataFrame({

        "Demand_MWh": [demand],

        "Wind_Generation_MWh": [wind],

        "Solar_Generation_MWh": [solar],

        "Gas_Price_EUR": [gas],

        "CO2_Price_EUR": [co2],

        "Temperature_C": [temperature]

    })


    if st.button(
        "Predict Electricity Price"
    ):

        prediction = model.predict(
            input_data
        )


        st.success(
            f"Predicted Price: {prediction[0]:.2f} €/MWh"
        )



# =========================
# Model Performance
# =========================

with tab3:

    st.subheader(
        "Random Forest Model Performance"
    )


    X = df.drop(
    columns=[
        "Electricity_Price_EUR",
        "Date"
    ],
    errors="ignore"
)


    y = df[
        "Electricity_Price_EUR"
    ]


    predictions = model.predict(
        X
    )


    mae = mean_absolute_error(
        y,
        predictions
    )


    rmse = mean_squared_error(
        y,
        predictions
    ) ** 0.5


    r2 = r2_score(
        y,
        predictions
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "MAE",
        f"{mae:.2f}"
    )


    c2.metric(
        "RMSE",
        f"{rmse:.2f}"
    )


    c3.metric(
        "R² Score",
        f"{r2:.3f}"
    )


    result = pd.DataFrame({

        "Actual": y,

        "Predicted": predictions

    })


    fig5 = px.line(
        result,
        title="Actual vs Predicted"
    )


    st.plotly_chart(
        fig5,
        width="stretch"
    )

    # =========================
    # Feature Importance
    # =========================

    st.subheader(
        "Feature Importance"
    )


    importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": model.feature_importances_

    })


    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )


    fig6 = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Factors Affecting Electricity Price"
    )


    st.plotly_chart(
        fig6,
        width="stretch"
    )


    st.info(
        f"""
        Main price driver:
        
        **{importance.iloc[0]['Feature']}**
        
        Importance:
        **{importance.iloc[0]['Importance']:.2%}**
        """
    )



# =========================
# Data
# =========================

with tab4:

    st.subheader(
        "Dataset Preview"
    )

    st.dataframe(
        df.head(20),
        width="stretch"
    )


st.divider()

st.caption(
    "Energy Price Forecasting Project | Python | SQL | Machine Learning | Streamlit"
)