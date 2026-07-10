SELECT

    YEAR(price_date) AS year,

    MONTH(price_date) AS month,

    ROUND(
        AVG(settlement_price),
        2
    ) AS avg_price,

    ROUND(
        MIN(settlement_price),
        2
    ) AS min_price,

    ROUND(
        MAX(settlement_price),
        2
    ) AS max_price,

    ROUND(
        STDDEV(settlement_price),
        2
    ) AS volatility

FROM market_prices

GROUP BY

    YEAR(price_date),
    MONTH(price_date)

ORDER BY

    year,
    month;
    
#Best & Worst Month
WITH monthly_prices AS (

SELECT

    YEAR(price_date) AS year,

    MONTH(price_date) AS month,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY

    YEAR(price_date),
    MONTH(price_date)

)

SELECT

    *,

    RANK()

    OVER(
        ORDER BY average_price DESC
    ) AS price_rank

FROM monthly_prices;