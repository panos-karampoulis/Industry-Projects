#What is the 7-day moving average of electricity prices?
WITH daily_prices AS (

    SELECT

        price_date,

        ROUND(AVG(settlement_price),2) AS average_price

    FROM market_prices

    GROUP BY price_date

)

SELECT

    price_date,

    average_price,

    ROUND(

        AVG(average_price)

        OVER(

            ORDER BY price_date

            ROWS BETWEEN 6 PRECEDING
            AND CURRENT ROW

        ),

    2) AS rolling_7_day_avg

FROM daily_prices

ORDER BY price_date;

#Rolling 30-Day Average
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

    ROUND(

        AVG(average_price)

        OVER(

            ORDER BY price_date

            ROWS BETWEEN 29 PRECEDING
            AND CURRENT ROW

        ),

    2) AS rolling_30_day_avg

FROM daily_prices;

#What was the highest market price observed up to each day?

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

    MAX(average_price)

    OVER(

        ORDER BY price_date

        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW

    ) AS running_max

FROM daily_prices;

#Running Minimum
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

    MIN(average_price)

    OVER(

        ORDER BY price_date

        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW

    ) AS running_min

FROM daily_prices;

#Which hours experienced unusually high electricity prices?
SELECT

    price_timestamp,

    settlement_price,

    CASE

        WHEN settlement_price >= 200
        THEN 'Extreme'

        WHEN settlement_price >=150
        THEN 'High'

        ELSE 'Normal'

    END AS price_category

FROM market_prices

ORDER BY settlement_price DESC;

#Monthly Price Ranking
WITH monthly_prices AS (

SELECT

    MONTH(price_date) AS month,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY MONTH(price_date)

)

SELECT

    month,

    average_price,

    RANK()

    OVER(

        ORDER BY average_price DESC

    ) AS monthly_rank

FROM monthly_prices;

#How many hours fall into each price range?
SELECT

    CASE

        WHEN settlement_price < 50
            THEN '<50'

        WHEN settlement_price <100
            THEN '50-100'

        WHEN settlement_price <150
            THEN '100-150'

        WHEN settlement_price <200
            THEN '150-200'

        ELSE '>200'

    END AS price_band,

    COUNT(*) AS observations

FROM market_prices

GROUP BY price_band

ORDER BY observations DESC;

#Most Volatile Days
SELECT

    price_date,

    ROUND(
        STDDEV(settlement_price),
        2
    ) AS volatility

FROM market_prices

GROUP BY price_date

ORDER BY volatility DESC

LIMIT 15;