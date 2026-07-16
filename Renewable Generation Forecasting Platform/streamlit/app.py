import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from src.predict import predict_generation
from pathlib import Path


# -----------------------
# Configuration
# -----------------------

st.set_page_config(
    page_title="Renewable Generation Forecast",
    page_icon="⚡",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent


COUNTRIES = sorted(
    [
        folder.name
        for folder in (BASE_DIR / "reports").iterdir()
        if (
            folder.is_dir()
            and
            (
                folder /
                "renewable_forecast_results.csv"
            ).exists()
        )
    ]
)

if not COUNTRIES:
    st.error(
        "No country reports found."
    )
    st.stop()


# -----------------------
# Load functions
# -----------------------


@st.cache_data
def load_metrics(country):

    file = (
        BASE_DIR
        /
        "reports"
        /
        country
        /
        "model_metrics.csv"
    )

    return pd.read_csv(file)



@st.cache_data
def load_data(country):

    forecast_file = (
        BASE_DIR
        /
        "reports"
        /
        country
        /
        "renewable_forecast_results.csv"
    )


    daily_file = (
        BASE_DIR
        /
        "reports"
        /
        country
        /
        "daily_summary.csv"
    )


    dataset_file = (
        BASE_DIR
        /
        "data"
        /
        "processed"
        /
        country
        /
        f"{country}_generation.csv"
    )


    forecast = pd.read_csv(
        forecast_file,
        parse_dates=["datetime"]
    )


    daily = pd.read_csv(
        daily_file
    )


    dataset = pd.read_csv(
        dataset_file,
        parse_dates=["datetime"]
    )


    return forecast, daily, dataset

@st.cache_data
def load_feature_importance(country):

    file = (
        BASE_DIR
        /
        "reports"
        /
        country
        /
        "feature_importance.csv"
    )

    return pd.read_csv(file)



@st.cache_data
def load_metadata(country):

    metadata_file = (
        BASE_DIR
        /
        "models"
        /
        country
        /
        "model_metadata.json"
    )


    with open(
        metadata_file,
        "r"
    ) as file:

        return json.load(file)

@st.cache_data
def load_weather(country):

    weather_file = (
        BASE_DIR
        /
        "data"
        /
        "weather"
        /
        country
        /
        "weather.csv"
    )

    weather = pd.read_csv(
        weather_file,
        parse_dates=["datetime"]
    )

    return weather




# -----------------------
# Country selection
# -----------------------

country = st.sidebar.selectbox(
    "Select country",
    COUNTRIES
)


forecast, daily, dataset = load_data(country)

metadata = load_metadata(country)


importance = load_feature_importance(country)

metrics = load_metrics(country)
weather = load_weather(country)

# -----------------------
# Feature Importance
# -----------------------

st.subheader(
    "Top Forecasting Drivers"
)


top_features = (
    importance
    .head(15)
    .sort_values(
        "importance"
    )
)


fig = px.bar(

    top_features,

    x="importance",

    y="feature",

    orientation="h",

    title="Top 15 Important Features"

)


fig.update_layout(
    height=600,
    template="plotly_white"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# Prediction Quality
# -----------------------

st.subheader(
    "Prediction Quality"
)


fig = px.scatter(

    forecast,

    x="renewable_total_mwh",

    y="prediction_mwh",

    opacity=0.5,

    labels={

        "renewable_total_mwh":
        "Actual MWh",

        "prediction_mwh":
        "Predicted MWh"

    }

)


fig.update_layout(
    template="plotly_white",
    height=500
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# Error Analysis
# -----------------------

st.subheader(
    "Forecast Error Analysis"
)


fig = px.line(

    forecast,

    x="datetime",

    y="absolute_error",

    title="Absolute Forecast Error"

)


fig.update_layout(

    template="plotly_white",

    height=400

)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -----------------------
# Header
# -----------------------

st.title(
    f"⚡ {country.title()} Renewable Generation Forecast"
)


st.write(
    "Machine Learning based Solar + Wind generation forecasting platform"
)



# -----------------------
# Model Performance
# -----------------------

st.subheader(
    "Model Performance"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Model",
        metadata["model"]
    )


with c2:

    st.metric(
        "Test Period",
        metadata["test_period"]
    )


with c3:

    st.metric(
        "MAE (MWh)",
        f'{metadata["MAE_MWh"]:,.0f}'
    )


with c4:

    st.metric(
        "R² Score",
        metadata["R2"]
    )



# -----------------------
# Energy Mix
# -----------------------

st.subheader(
    "Renewable Generation Mix"
)


solar_total = dataset["solar_mwh"].sum()

wind_total = dataset["wind_total_mwh"].sum()


total_generation = solar_total + wind_total


solar_share = (
    solar_total /
    total_generation *
    100
)


wind_share = (
    wind_total /
    total_generation *
    100
)



m1, m2 = st.columns(2)

mix = pd.DataFrame({

    "Source": ["Solar", "Wind"],

    "Generation": [
        solar_total,
        wind_total
    ]

})

fig = px.pie(

    mix,

    names="Source",

    values="Generation",

    hole=0.45

)

fig.update_layout(
    height=420
)

st.plotly_chart(
    fig,
    use_container_width=True
)


with m1:

    st.metric(
        "Solar Contribution",
        f"{solar_share:.1f}%"
    )


with m2:

    st.metric(
        "Wind Contribution",
        f"{wind_share:.1f}%"
    )



# -----------------------
# Forecast Accuracy
# -----------------------

st.subheader(
    "Forecast Accuracy"
)


accuracy = (
    1 -
    (
        forecast["absolute_error"]
        /
        forecast["renewable_total_mwh"]
    )
)


accuracy = accuracy.mean() * 100



st.metric(
    "Overall Forecast Accuracy",
    f"{accuracy:.2f}%"
)

fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=accuracy,

        title={"text": "Forecast Accuracy (%)"},

        gauge={

            "axis": {"range": [0, 100]},

            "bar": {"thickness": 0.35},

            "steps": [

                {"range": [0, 70], "color": "#ffcccc"},

                {"range": [70, 90], "color": "#ffe699"},

                {"range": [90, 100], "color": "#c6efce"}

            ]

        }

    )

)

fig.update_layout(
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# Forecast Explorer
# -----------------------

st.sidebar.header(
    "Forecast Explorer"
)


selected_date = st.sidebar.date_input(
    "Select Date",
    forecast["datetime"].dt.date.min()
)


daily_forecast = forecast[
    forecast["datetime"].dt.date == selected_date
]



st.subheader(
    f"Hourly Forecast - {selected_date}"
)



if not daily_forecast.empty:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_forecast["datetime"],
            y=daily_forecast["renewable_total_mwh"],
            mode="lines",
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=daily_forecast["datetime"],
            y=daily_forecast["prediction_mwh"],
            mode="lines",
            name="Prediction"
        )
    )

    fig.update_layout(

        title="Hourly Renewable Generation",

        xaxis_title="Hour",

        yaxis_title="MWh",

        hovermode="x unified",

        template="plotly_white",

        height=450

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------
# Weather Analytics
# -----------------------

st.subheader(
    "Weather Conditions"
)


weather_daily = weather.copy()


w1, w2, w3 = st.columns(3)


with w1:

    st.metric(
        "Average Temperature",
        f"{weather['temperature'].mean():.1f} °C"
    )


with w2:

    st.metric(
        "Average Wind Speed",
        f"{weather['wind_speed'].mean():1f} km/h"
    )


with w3:

    st.metric(
        "Average Solar Radiation",
        f"{weather['solar_radiation'].mean():.1f}"
    )



fig = px.line(
    weather,
    x="datetime",
    y="temperature",
    title="Temperature"
)

fig.update_layout(
    template="plotly_white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)



fig = px.line(
    weather,
    x="datetime",
    y="solar_radiation",
    title="Solar Radiation"
)

fig.update_layout(
    template="plotly_white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)



fig = px.line(
    weather,
    x="datetime",
    y="wind_speed",
    title="Wind Speed"
)

fig.update_layout(
    template="plotly_white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------
# Weather Impact Analysis
# -----------------------

st.subheader(
    "Weather Impact on Renewable Generation"
)


weather_generation = pd.merge(
    dataset,
    weather,
    on="datetime",
    how="inner"
)


fig = px.scatter(
    weather_generation,
    x="solar_radiation",
    y="solar_mwh",
    opacity=0.4,
    title="Solar Radiation vs Solar Generation",
    labels={
        "solar_radiation": "Solar Radiation",
        "solar_mwh": "Solar Generation MWh"
    }
)


fig.update_layout(
    template="plotly_white",
    height=450
)


st.plotly_chart(
    fig,
    use_container_width=True
)


fig = px.scatter(
    weather_generation,
    x="wind_speed",
    y="wind_total_mwh",
    opacity=0.4,
    title="Wind Speed vs Wind Generation",
    labels={
        "wind_speed": "Wind Speed km/h",
        "wind_total_mwh": "Wind Generation MWh"
    }
)


fig.update_layout(
    template="plotly_white",
    height=450
)


st.plotly_chart(
    fig,
    use_container_width=True
)





# -----------------------
# Insights
# -----------------------

st.subheader(
    "Energy Analytics Insights"
)


st.info(
f"""
**Key Findings**

• Model:
  {metadata["model"]}

• Performance:
  - MAE: {metadata["MAE_MWh"]:.0f} MWh
  - R²: {metadata["R2"]}

• Renewable mix:
  - Solar: {solar_share:.1f}%
  - Wind: {wind_share:.1f}%

• Framework ready for additional countries.
"""
)

# -----------------------
# Country Comparison
# -----------------------

st.subheader(
    "Country Model Comparison"
)


comparison = []


for c in COUNTRIES:

    try:

        metric = load_metrics(c)

        comparison.append({

            "Country": c.title(),

            "MAE":
            metric["MAE"].iloc[0],

            "RMSE":
            metric["RMSE"].iloc[0],

            "R2":
            metric["R2"].iloc[0]

        })


    except:

        pass



comparison_df = pd.DataFrame(
    comparison
)


if not comparison_df.empty:


    fig = px.bar(

        comparison_df,

        x="Country",

        y="MAE",

        title="MAE Comparison (Lower is Better)"

    )


    fig.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    fig2 = px.bar(

        comparison_df,

        x="Country",

        y="R2",

        title="Model R² Comparison"

    )


    fig2.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# -----------------------
# Forecast Button
# -----------------------

st.subheader(
    "Renewable Generation Forecast"
)


available_dates = (
    pd.to_datetime(
        forecast["datetime"]
    )
    .dt.date
    .unique()
)


selected_forecast_date = st.date_input(
    "Select forecast date",
    available_dates[-1]
)


if st.button(
    "⚡ Run Forecast"
):

    with st.spinner(
        "Generating prediction..."
    ):

        forecast_future = predict_generation(
            country,
            selected_forecast_date
        )


    st.success(
        "Forecast completed"
    )


    # -----------------------
    # Forecast Metrics
    # -----------------------

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "☀ Solar Generation",
            f"{forecast_future['solar_mwh'].sum():,.0f} MWh"
        )


    with c2:

        st.metric(
            "🌬 Wind Generation",
            f"{forecast_future['wind_total_mwh'].sum():,.0f} MWh"
        )


    with c3:

        st.metric(
            "⚡ Predicted Renewable",
            f"{forecast_future['prediction_mwh'].sum():,.0f} MWh"
        )


    # -----------------------
    # Prediction Chart
    # -----------------------

    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=forecast_future["datetime"],
            y=forecast_future["prediction_mwh"],
            mode="lines+markers",
            name="Prediction"
        )
    )


    fig.update_layout(
        title="Hourly Renewable Forecast",
        xaxis_title="Time",
        yaxis_title="MWh",
        template="plotly_white",
        height=450
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------
    # Actual vs Prediction
    # -----------------------

    fig2 = go.Figure()


    fig2.add_trace(
        go.Scatter(
            x=forecast_future["datetime"],
            y=forecast_future["renewable_total_mwh"],
            mode="lines",
            name="Actual"
        )
    )


    fig2.add_trace(
        go.Scatter(
            x=forecast_future["datetime"],
            y=forecast_future["prediction_mwh"],
            mode="lines",
            name="Prediction"
        )
    )


    fig2.update_layout(
        title="Actual vs Forecast Renewable Generation",
        xaxis_title="Time",
        yaxis_title="MWh",
        template="plotly_white",
        height=450
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # -----------------------
    # Forecast Error
    # -----------------------

    forecast_error = (
        forecast_future["absolute_error"]
        .mean()
    )


    st.metric(
        "Average Forecast Error",
        f"{forecast_error:,.0f} MWh"
    )


    # -----------------------
    # Save for Download
    # -----------------------

    csv = forecast_future.to_csv(
        index=False
    )


    st.download_button(
        "Download Forecast CSV",
        csv,
        "renewable_forecast.csv",
        "text/csv"
    )