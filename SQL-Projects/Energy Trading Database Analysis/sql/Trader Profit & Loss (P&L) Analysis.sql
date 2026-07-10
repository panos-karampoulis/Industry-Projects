#Which traders have the largest profit or loss from their trades?
WITH trade_pnl AS (

    SELECT

        tr.trade_id,

        tr.trader_id,

        tr.trade_type,

        tr.volume_mwh,

        tr.price,

        CASE
            WHEN tr.trade_type = 'SELL'
            THEN tr.volume_mwh * tr.price

            WHEN tr.trade_type = 'BUY'
            THEN -(tr.volume_mwh * tr.price)

        END AS pnl_value


    FROM trades tr

)

SELECT *

FROM trade_pnl

LIMIT 20;

WITH trade_pnl AS (

    SELECT

        trader_id,

        CASE
            WHEN trade_type = 'SELL'
            THEN volume_mwh * price

            WHEN trade_type = 'BUY'
            THEN -(volume_mwh * price)

        END AS pnl_value


    FROM trades

)


SELECT

    t.trader_name,

    ROUND(
        SUM(tp.pnl_value),
        2
    ) AS total_pnl


FROM trade_pnl tp

JOIN traders t
ON tp.trader_id = t.trader_id


GROUP BY t.trader_name

ORDER BY total_pnl DESC;

#Have traders bought or sold a larger volume?
SELECT

    t.trader_name,

    tr.trade_type,

    ROUND(
        SUM(tr.volume_mwh),
        2
    ) AS volume_mwh


FROM trades tr

JOIN traders t
ON tr.trader_id = t.trader_id


GROUP BY

    t.trader_name,
    tr.trade_type


ORDER BY

    t.trader_name;
    
#Net Position per Trader
SELECT

    t.trader_name,

    SUM(
        CASE
            WHEN tr.trade_type='SELL'
            THEN tr.volume_mwh

            WHEN tr.trade_type='BUY'
            THEN -tr.volume_mwh

        END
    ) AS net_position_mwh


FROM trades tr

JOIN traders t
ON tr.trader_id=t.trader_id


GROUP BY t.trader_name

ORDER BY net_position_mwh DESC;