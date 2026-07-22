import vectorbt as vbt



def run_backtest(
        close,
        signals,
        size=None,
        sl_stop=None,
        tp_stop=None
):


    entries = (
        signals["position"]
        .diff()
        == 1
    )


    exits = (
        signals["position"]
        .diff()
        == -1
    )



    portfolio = vbt.Portfolio.from_signals(

        close,

        entries,

        exits,

        size=size,

        size_type="Percent",

        sl_stop=sl_stop,

        tp_stop=tp_stop,

        init_cash=10000,

        fees=0.001,

        freq="1D"

    )


    return portfolio




def get_performance(
        portfolio
):

    stats = {

        "Total Return":
            portfolio.total_return(),

        "Sharpe Ratio":
            portfolio.sharpe_ratio(
                freq="1D"
            ),

        "Max Drawdown":
            portfolio.max_drawdown(),

        "Trades":
            portfolio.trades.count()

    }


    return stats