from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)

from app.backtester import run_backtest

from app.attribution import (
    calculate_return_contribution,
    calculate_risk_contribution,
    correlation_matrix
)

import pandas as pd



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)



strategies = {


"SMA":
sma_crossover_strategy(df),


"RSI":
rsi_mean_reversion(df),


"Momentum":
momentum_strategy(df)

}



returns = {}



for name, signal in strategies.items():


    pf = run_backtest(

        df["Close"],

        signal

    )


    returns[name] = pf.returns()



strategy_returns = pd.DataFrame(
    returns
)



weights = {


"SMA":1/3,

"RSI":1/3,

"Momentum":1/3

}



print(
    "\nRETURN CONTRIBUTION"
)


print(

calculate_return_contribution(

    strategy_returns,

    weights

)

)



print(
    "\nRISK CONTRIBUTION"
)


print(

calculate_risk_contribution(

    strategy_returns,

    weights

)

)



print(
    "\nCORRELATION MATRIX"
)


print(

correlation_matrix(

    strategy_returns

)

)