#What is the average price over the last 24 hours at any given moment?
SELECT
    price_timestamp,
    settlement_price,

    ROUND(
        AVG(settlement_price)
        OVER(
            ORDER BY price_timestamp
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ),
    2) AS rolling_24h_avg

FROM market_prices
ORDER BY price_timestamp;

#Which times of the day are the most expensive?
SELECT

    hour,

    ROUND(AVG(settlement_price),2)
    AS avg_hourly_price

FROM market_prices

GROUP BY hour

ORDER BY avg_hourly_price DESC;

#How much did the price change compared to the previous hour?
SELECT

    price_timestamp,

    settlement_price,

    LAG(settlement_price)
    OVER(
        ORDER BY price_timestamp
    ) AS previous_price,

    ROUND(
        settlement_price -
        LAG(settlement_price)
        OVER(
            ORDER BY price_timestamp
        ),
    2) AS price_change


FROM market_prices;
#What were the three most expensive hours of each month?
WITH ranked_prices AS (

SELECT

    price_timestamp,

    MONTH(price_date) AS month,

    settlement_price,

    RANK()
    OVER(
        PARTITION BY MONTH(price_date)
        ORDER BY settlement_price DESC
    ) AS price_rank


FROM market_prices

)

SELECT *

FROM ranked_prices

WHERE price_rank <= 3

ORDER BY month, price_rank;