import pandas as pd

from .spread import (
    estimate_hedge_ratio,
    calculate_spread,
    calculate_zscore
)

from .signals import (
    generate_signals
)

from .backtest import (
    calculate_strategy_returns,
    performance_summary
)

from .costs import (
    apply_transaction_costs
)


def backtest_pair(
    series_y,
    series_x,
    name_y,
    name_x
):

    alpha, beta = estimate_hedge_ratio(
    series_y,
    series_x
    )

    spread = calculate_spread(
        series_y,
        series_x,
        beta
    )


    zscore = calculate_zscore(
        spread
    )


    signals = generate_signals(
        zscore
    )


    returns = calculate_strategy_returns(
        series_y,
        series_x,
        beta,
        signals["Position"]
    )


    net_returns = apply_transaction_costs(
        returns,
        signals["Position"]
    )


    result = performance_summary(
        net_returns
    )


    result["Pair"] = (
        name_y
        +
        "-"
        +
        name_x
    )


    result["Trades"] = (
        signals["Position"]
        .diff()
        .abs()
        .sum()
    )


    return result