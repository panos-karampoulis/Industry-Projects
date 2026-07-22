import pandas as pd

from src.market_data import download_prices
from src.returns import calculate_returns

from src.factor_portfolios import (
    momentum_scores,
    volatility_scores,
    select_top_assets
)

from src.value_factor import calculate_hml_exposures

from src.factor_analysis import factor_performance_table


def run_factor_pipeline(
        tickers,
        start_date,
        end_date,
        n_assets=5
):

    # Prices

    prices = download_prices(
        tickers,
        start_date,
        end_date
    )


    # Returns

    returns = calculate_returns(
        prices
    )


    # ------------------
    # Momentum
    # ------------------

    mom_scores = momentum_scores(
        prices
    )


    momentum_assets = select_top_assets(
        mom_scores,
        n=n_assets
    )


    momentum_returns = (
        returns[momentum_assets]
        .mean(axis=1)
    )


    # ------------------
    # Low Volatility
    # ------------------

    vol_scores = volatility_scores(
        returns
    )


    low_vol_assets = select_top_assets(
        vol_scores,
        n=n_assets,
        ascending=True
    )


    low_vol_returns = (
        returns[low_vol_assets]
        .mean(axis=1)
    )


    # ------------------
    # Value
    # ------------------

    # προσωρινά θα χρησιμοποιήσουμε
    # το υπάρχον factor data

    from src.factor_data import load_fama_french


    factors = load_fama_french()


    hml_scores = calculate_hml_exposures(
        returns,
        factors
    )


    hml_series = pd.Series(
        hml_scores
    )


    value_assets = (
        hml_series
        .sort_values(
            ascending=False
        )
        .head(n_assets)
        .index
        .tolist()
    )


    value_returns = (
        returns[value_assets]
        .mean(axis=1)
    )


    # ------------------
    # Benchmark
    # ------------------

    market_returns = returns["SPY"]


    portfolios = {

        "Market (SPY)": market_returns,

        "Momentum": momentum_returns,

        "Value": value_returns,

        "Low Volatility": low_vol_returns

    }


    table = factor_performance_table(
        portfolios
    )


    assets = {

        "Momentum": momentum_assets,

        "Value": value_assets,

        "Low Volatility": low_vol_assets

    }


    return {

        "prices": prices,

        "returns": returns,

        "portfolios": portfolios,

        "performance": table,

        "assets": assets,

        "factors": factors

    }