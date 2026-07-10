######How many trades were executed?
SELECT

COUNT(*) AS total_trades

FROM fact_trades;

############How much energy was traded?
SELECT

ROUND(
SUM(volume_mwh),
2
) AS total_volume_mwh

FROM fact_trades;

###################What is the total monetary value of transactions?
SELECT

ROUND(
SUM(trade_value),
2
) AS total_trade_value

FROM fact_trades;


#############TRADING VOLUME BY TYPE
SELECT

trade_type,

ROUND(
SUM(volume_mwh),
2
) AS total_volume

FROM fact_trades

GROUP BY trade_type;


############# NET TRADING P&L
SELECT


ROUND(

SUM(

CASE

WHEN trade_type = 'SELL'
THEN trade_value

WHEN trade_type = 'BUY'
THEN -trade_value

END

),

2

) AS net_pnl


FROM fact_trades;


################## TOP TRADERS BY P&L
SELECT


t.trader_name,


ROUND(

SUM(

CASE

WHEN f.trade_type='SELL'
THEN f.trade_value

WHEN f.trade_type='BUY'
THEN -f.trade_value

END

),

2

) AS pnl


FROM fact_trades f


JOIN dim_trader t

ON f.trader_key=t.trader_key


GROUP BY t.trader_name


ORDER BY pnl DESC;


############ Trading Volume by Market
SELECT

m.market_name,

ROUND(
SUM(f.volume_mwh),
2
) AS volume_mwh


FROM fact_trades f


JOIN dim_market m

ON f.market_key=m.market_key


GROUP BY m.market_name


ORDER BY volume_mwh DESC;


###########Which assets generate the most trading activity?
SELECT

a.asset_name,

a.asset_type,

ROUND(
SUM(f.volume_mwh),
2
) AS traded_volume


FROM fact_trades f


JOIN dim_asset a

ON f.asset_key=a.asset_key


GROUP BY

a.asset_name,

a.asset_type


ORDER BY traded_volume DESC;


############Renewable vs Non-Renewable
SELECT

CASE

WHEN a.renewable = 1
THEN 'Renewable'

ELSE 'Non Renewable'

END AS energy_type,


ROUND(

SUM(f.volume_mwh),

2

) AS total_volume


FROM fact_trades f


JOIN dim_asset a

ON f.asset_key=a.asset_key


GROUP BY energy_type;