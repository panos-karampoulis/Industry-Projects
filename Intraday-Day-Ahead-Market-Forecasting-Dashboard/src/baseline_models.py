import pandas as pd

from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing,
    ExponentialSmoothing
)

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.tsa.statespace.sarimax import SARIMAX



# ============================================================
# NAIVE
# ============================================================

def naive_forecast(train, test):

    last_value = train.iloc[-1]

    forecast = pd.Series(
        last_value,
        index=test.index
    )

    return forecast



# ============================================================
# MOVING AVERAGE
# ============================================================

def moving_average_forecast(
    train,
    test,
    window=96
):

    mean_value = (
        train
        .tail(window)
        .mean()
    )

    forecast = pd.Series(
        mean_value,
        index=test.index
    )

    return forecast



# ============================================================
# SIMPLE EXPONENTIAL SMOOTHING
# ============================================================

def simple_exponential_smoothing_forecast(
    train,
    test
):

    model = SimpleExpSmoothing(
        train,
        initialization_method="estimated"
    )

    fitted = model.fit(
        optimized=True
    )

    forecast = fitted.forecast(
        len(test)
    )

    forecast.index = test.index

    return forecast



# ============================================================
# HOLT-WINTERS
# ============================================================

def holt_winters_forecast(
    train,
    test
):

    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add",
        seasonal_periods=96,
        initialization_method="estimated"
    )


    fitted = model.fit(
        optimized=True
    )


    forecast = fitted.forecast(
        len(test)
    )


    forecast.index = test.index


    return forecast



# ============================================================
# ARIMA
# ============================================================

def arima_forecast(
    train,
    test,
    window=5000
):

    train_small = train.tail(window)


    model = ARIMA(
        train_small,
        order=(2,1,2)
    )


    fitted = model.fit()


    forecast = fitted.forecast(
        len(test)
    )


    forecast.index = test.index


    return forecast



# ============================================================
# SARIMA
# ============================================================

def sarima_forecast(
    train,
    test,
    window=2000
):


    train_small = train.tail(window)


    model = SARIMAX(
        train_small,
        order=(1,1,1),
        seasonal_order=(0,1,1,96),
        enforce_stationarity=False,
        enforce_invertibility=False
    )


    fitted = model.fit(
        disp=False,
        maxiter=50
    )


    forecast = fitted.forecast(
        len(test)
    )


    forecast.index = test.index


    return forecast