#Which traders handle the largest volume of energy?
SELECT

    t.trader_name,

    ROUND(
        SUM(tr.volume_mwh),
        2
    ) AS total_volume_mwh

FROM trades tr

JOIN traders t
ON tr.trader_id = t.trader_id

GROUP BY t.trader_name

ORDER BY total_volume_mwh DESC;
#Which trader executes the most trades?
SELECT

    t.trader_name,

    COUNT(*) AS number_of_trades

FROM trades tr

JOIN traders t
ON tr.trader_id = t.trader_id

GROUP BY t.trader_name

ORDER BY number_of_trades DESC;

#In which market do we have the greatest activity?
SELECT

    m.market_name,

    ROUND(
        SUM(tr.volume_mwh),
        2
    ) AS total_volume_mwh

FROM trades tr

JOIN markets m
ON tr.market_id = m.market_id

GROUP BY m.market_name

ORDER BY total_volume_mwh DESC;

#Which assets have the highest trading activity?
SELECT

    a.asset_name,

    a.asset_type,

    ROUND(
        SUM(tr.volume_mwh),
        2
    ) AS traded_volume

FROM trades tr

JOIN assets a
ON tr.asset_id = a.asset_id

GROUP BY
    a.asset_name,
    a.asset_type

ORDER BY traded_volume DESC;