WITH trading_summary AS (

    SELECT

        tr.trader_id,

        tr.market_id,

        tr.asset_id,

        COUNT(*) AS number_of_trades,

        SUM(tr.volume_mwh) AS total_volume,


        SUM(

            CASE

                WHEN tr.trade_type='SELL'
                THEN tr.volume_mwh * tr.price


                WHEN tr.trade_type='BUY'
                THEN -(tr.volume_mwh * tr.price)


            END

        ) AS pnl


    FROM trades tr


    GROUP BY

        tr.trader_id,
        tr.market_id,
        tr.asset_id

)


SELECT


    t.trader_name,

    m.market_name,

    a.asset_name,


    ts.number_of_trades,


    ROUND(
        ts.total_volume,
        2
    ) AS total_volume_mwh,


    ROUND(
        ts.pnl,
        2
    ) AS pnl,


    RANK()

    OVER(

        PARTITION BY t.trader_name

        ORDER BY ts.pnl DESC

    ) AS pnl_rank



FROM trading_summary ts


JOIN traders t
ON ts.trader_id=t.trader_id


JOIN markets m
ON ts.market_id=m.market_id


JOIN assets a
ON ts.asset_id=a.asset_id


ORDER BY

t.trader_name,

pnl_rank;