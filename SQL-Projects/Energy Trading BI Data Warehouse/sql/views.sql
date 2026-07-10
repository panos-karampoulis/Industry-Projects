#DAILY MARKET SUMMARY
USE energy_trading_db;

DROP VIEW IF EXISTS vw_daily_market_summary;

CREATE VIEW vw_daily_market_summary AS

SELECT

    price_date,

    ROUND(AVG(settlement_price),2) AS average_price,

    ROUND(MIN(settlement_price),2) AS minimum_price,

    ROUND(MAX(settlement_price),2) AS maximum_price,

    ROUND(STDDEV(settlement_price),2) AS volatility,

    COUNT(*) AS hourly_observations

FROM market_prices

GROUP BY price_date;

SELECT *
FROM vw_daily_market_summary;

#TRADER PERFORMANCE
DROP VIEW IF EXISTS vw_trader_performance;

CREATE VIEW vw_trader_performance AS

SELECT

    t.trader_name,

    COUNT(*) AS total_trades,

    SUM(tr.volume_mwh) AS total_volume,

    ROUND(

        SUM(

            CASE

                WHEN tr.trade_type='SELL'
                THEN tr.volume_mwh*tr.price

                WHEN tr.trade_type='BUY'
                THEN -(tr.volume_mwh*tr.price)

            END

        ),

    2) AS pnl

FROM trades tr

JOIN traders t

ON tr.trader_id=t.trader_id

GROUP BY t.trader_name;

SELECT *
FROM vw_trader_performance
ORDER BY pnl DESC;

#MONTHLY MARKET SUMMARY
DROP VIEW IF EXISTS vw_monthly_market_summary;

CREATE VIEW vw_monthly_market_summary AS

SELECT

    YEAR(price_date) AS year,

    MONTH(price_date) AS month,

    ROUND(AVG(settlement_price),2) AS average_price,

    ROUND(STDDEV(settlement_price),2) AS volatility

FROM market_prices

GROUP BY

    YEAR(price_date),

    MONTH(price_date);