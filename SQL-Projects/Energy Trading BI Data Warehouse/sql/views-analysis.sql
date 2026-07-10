USE energy_dw;


DROP VIEW IF EXISTS vw_executive_dashboard;


CREATE VIEW vw_executive_dashboard AS


SELECT


COUNT(*) AS total_trades,


ROUND(
SUM(volume_mwh),
2
) AS total_volume_mwh,


ROUND(
SUM(trade_value),
2
) AS total_trade_value,


ROUND(

SUM(

CASE

WHEN trade_type='SELL'
THEN trade_value

WHEN trade_type='BUY'
THEN -trade_value

END

),

2

) AS net_pnl


FROM fact_trades;


############### TRADER PERFORMANCE
DROP VIEW IF EXISTS vw_trader_performance;


CREATE VIEW vw_trader_performance AS


SELECT


t.trader_name,


COUNT(f.trade_key) AS total_trades,


ROUND(
SUM(f.volume_mwh),
2
) AS volume_mwh,


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


GROUP BY t.trader_name;

########### MONTHLY TRADING PERFORMANCE
DROP VIEW IF EXISTS vw_monthly_performance;


CREATE VIEW vw_monthly_performance AS


SELECT


d.year_number,

d.month_name,


ROUND(
SUM(f.volume_mwh),
2
) AS volume_mwh,


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


JOIN dim_date d

ON f.date_key=d.date_key


GROUP BY

d.year_number,

d.month_number,

d.month_name;

######### RENEWABLE ENERGY ANALYSIS
DROP VIEW IF EXISTS vw_renewable_analysis;


CREATE VIEW vw_renewable_analysis AS


SELECT


CASE

WHEN a.renewable=1

THEN 'Renewable'

ELSE 'Non Renewable'

END AS energy_type,


ROUND(
SUM(f.volume_mwh),
2
) AS traded_volume,


ROUND(
SUM(f.trade_value),
2
) AS trade_value


FROM fact_trades f


JOIN dim_asset a

ON f.asset_key=a.asset_key


GROUP BY energy_type;


USE energy_dw;


DROP VIEW IF EXISTS vw_market_analysis;


CREATE VIEW vw_market_analysis AS


SELECT

    m.market_name,

    COUNT(f.trade_key) AS total_trades,

    ROUND(
        SUM(f.volume_mwh),
        2
    ) AS total_volume_mwh,


    ROUND(
        SUM(f.trade_value),
        2
    ) AS total_trade_value,


    ROUND(
        AVG(f.trade_price),
        2
    ) AS average_trade_price


FROM fact_trades f


JOIN dim_market m

ON f.market_key = m.market_key


GROUP BY

m.market_name;

################## ASSET ANALYSIS
DROP VIEW IF EXISTS vw_asset_analysis;


CREATE VIEW vw_asset_analysis AS


SELECT


    a.asset_name,

    a.asset_type,


    CASE

        WHEN a.renewable = 1

        THEN 'Renewable'

        ELSE 'Non Renewable'

    END AS energy_type,


    ROUND(
        SUM(f.volume_mwh),
        2
    ) AS traded_volume_mwh,


    ROUND(
        SUM(f.trade_value),
        2
    ) AS traded_value,


    COUNT(f.trade_key) AS total_trades


FROM fact_trades f


JOIN dim_asset a

ON f.asset_key = a.asset_key


GROUP BY

a.asset_name,

a.asset_type,

energy_type;