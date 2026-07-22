import pandas as pd

from app.optimizer import optimize_sma_strategy
from app.strategies import sma_crossover_strategy
from app.backtester import run_backtest
from app.evaluation import generate_performance_report



def walk_forward_analysis(
        df,
        train_years=3,
        test_years=1,
        fast_windows=[20,30,50,70],
        slow_windows=[100,150,200,300]
):


    results = []

    equity_curves = []



    start_year = df.index.year.min()

    end_year = df.index.year.max()



    current_year = start_year



    while current_year + train_years + test_years <= end_year:


        train_start = current_year

        train_end = current_year + train_years


        test_start = train_end

        test_end = train_end + test_years



        print(
            f"""
            Training:
            {train_start}-{train_end}

            Testing:
            {test_start}-{test_end}
            """
        )



        train = df[

            (df.index.year >= train_start)
            &
            (df.index.year < train_end)

        ]



        test = df[

            (df.index.year >= test_start)
            &
            (df.index.year < test_end)

        ]



        if len(test)==0:

            break



        # =====================
        # Optimize TRAIN
        # =====================


        optimization = optimize_sma_strategy(

            train,

            fast_windows,

            slow_windows

        )



        best = (

            optimization

            .sort_values(
                "Sharpe",
                ascending=False
            )

            .iloc[0]

        )



        best_fast = int(
            best["Fast SMA"]
        )


        best_slow = int(
            best["Slow SMA"]
        )



        # =====================
        # Apply on TEST
        # =====================


        test_data = test.copy()



        test_data["SMA_FAST"] = (

            test_data["Close"]

            .rolling(best_fast)

            .mean()

        )



        test_data["SMA_SLOW"] = (

            test_data["Close"]

            .rolling(best_slow)

            .mean()

        )



        signals = pd.DataFrame(
            index=test_data.index
        )


        signals["position"] = 0


        signals.loc[

            test_data["SMA_FAST"]
            >
            test_data["SMA_SLOW"],

            "position"

        ] = 1



        portfolio = run_backtest(

            test_data["Close"],

            signals

        )



        report = generate_performance_report(

            portfolio

        )



        results.append(

            {

            "Train Period":
                f"{train_start}-{train_end}",

            "Test Period":
                f"{test_start}-{test_end}",

            "Fast SMA":
                best_fast,

            "Slow SMA":
                best_slow,

            "Return":
                report["Total Return"],

            "Sharpe":
                report["Sharpe Ratio"],

            "Drawdown":
                report["Maximum Drawdown"]

            }

        )



        current_year += test_years



    return pd.DataFrame(results)