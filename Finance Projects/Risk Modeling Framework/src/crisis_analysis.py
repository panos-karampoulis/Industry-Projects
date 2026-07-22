def analyze_crisis(
    portfolio_returns,
    start_date,
    end_date
):

    cumulative = (
        1 + portfolio_returns
    ).cumprod()


    crisis = portfolio_returns.loc[
        start_date:end_date
    ]


    if len(crisis)==0:
        return None



    peak_before = cumulative.loc[
        :start_date
    ].max()


    crisis_curve = cumulative.loc[
        start_date:end_date
    ]


    drawdown = (
        crisis_curve - peak_before
    ) / peak_before


    max_drawdown = drawdown.min()


    total_return = (
        crisis_curve.iloc[-1]
        /
        peak_before
    ) - 1


    worst_day = crisis.min()



    bottom_date = (
        crisis_curve.idxmin()
    )



    recovery_period = cumulative.loc[
        bottom_date:
    ]


    recovery = recovery_period[
        recovery_period >= peak_before
    ]


    recovery_days = None


    if len(recovery)>0:

        recovery_days = (
            recovery.index[0]
            -
            bottom_date
        ).days



    return {

        "Total Return":
            total_return,

        "Maximum Drawdown":
            max_drawdown,

        "Worst Day":
            worst_day,

        "Recovery Days":
            recovery_days,

        "Bottom Date":
            bottom_date

    }