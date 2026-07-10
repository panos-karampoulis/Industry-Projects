###What was the daily electricity market performance?
-- ==========================================================
-- Daily Market Summary
-- ==========================================================
SELECT

    price_date,

    ROUND(AVG(settlement_price),2) AS avg_price,

    ROUND(MIN(settlement_price),2) AS min_price,

    ROUND(MAX(settlement_price),2) AS max_price,

    ROUND(STDDEV(settlement_price),2) AS volatility,

    COUNT(*) AS hourly_observations

FROM market_prices

GROUP BY price_date

ORDER BY price_date;

#How did peak and off-peak prices differ each day?

SELECT

    price_date,

    peak_type,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price,

    ROUND(
        MAX(settlement_price),
        2
    ) AS highest_price

FROM market_prices

GROUP BY

    price_date,
    peak_type

ORDER BY

    price_date,
    peak_type;
    
#Which days experienced the largest intraday price movements?
SELECT

    price_date,

    ROUND(MAX(settlement_price),2) AS max_price,

    ROUND(MIN(settlement_price),2) AS min_price,

    ROUND(
        MAX(settlement_price)
        -
        MIN(settlement_price),
        2
    ) AS price_range

FROM market_prices

GROUP BY price_date

ORDER BY price_range DESC;

#top10 most expensive days
SELECT

    price_date,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY price_date

ORDER BY average_price DESC

LIMIT 10;

#top10 most cheap days
SELECT

    price_date,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY price_date

ORDER BY average_price

LIMIT 10;

#Was today's average price higher or lower than the previous day's?
WITH daily_prices AS (

SELECT

    price_date,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY price_date

)

SELECT

    price_date,

    average_price,

    LAG(average_price)
    OVER(
        ORDER BY price_date
    ) AS previous_day,

    ROUND(
        average_price
        -
        LAG(average_price)
        OVER(
            ORDER BY price_date),
    2) AS daily_change

FROM daily_prices;