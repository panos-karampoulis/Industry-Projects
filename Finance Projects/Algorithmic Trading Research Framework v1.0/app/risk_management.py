import pandas as pd



def fixed_position_size(
        signals,
        allocation=0.20
):

    """
    Fixed allocation position sizing
    """

    positions = (
        signals["position"]
        *
        allocation
    )

    return positions





def calculate_stop_loss(
        close,
        entries,
        stop_loss=0.10
):

    """
    Creates stop loss levels

    Example:
    Entry price = 100
    stop_loss = 10%

    Stop price = 90
    """


    stop_price = pd.Series(
        index=close.index,
        dtype=float
    )


    entry_price = None


    for i in range(len(close)):

        if entries.iloc[i]:

            entry_price = close.iloc[i]


        if entry_price:

            stop_price.iloc[i] = (
                entry_price
                *
                (1-stop_loss)
            )


    return stop_price






def calculate_take_profit(
        close,
        entries,
        take_profit=0.20
):

    """
    Creates take profit levels
    """


    target_price = pd.Series(
        index=close.index,
        dtype=float
    )


    entry_price = None


    for i in range(len(close)):

        if entries.iloc[i]:

            entry_price = close.iloc[i]


        if entry_price:

            target_price.iloc[i] = (
                entry_price
                *
                (1+take_profit)
            )


    return target_price