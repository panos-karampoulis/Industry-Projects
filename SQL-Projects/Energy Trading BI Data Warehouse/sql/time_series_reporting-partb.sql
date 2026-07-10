#How did electricity prices evolve each week?
SELECT

    YEAR(price_date) AS year,

    WEEK(price_date, 1) AS week_number,

    ROUND(AVG(settlement_price),2) AS avg_price,

    ROUND(MIN(settlement_price),2) AS min_price,

    ROUND(MAX(settlement_price),2) AS max_price,

    ROUND(STDDEV(settlement_price),2) AS volatility,

    COUNT(*) AS observations

FROM market_prices

GROUP BY

    YEAR(price_date),
    WEEK(price_date,1)

ORDER BY

    year,
    week_number;
    
#Highest Price Weeks

SELECT

    YEAR(price_date) AS year,

    WEEK(price_date,1) AS week_number,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY

    YEAR(price_date),
    WEEK(price_date,1)

ORDER BY average_price DESC

LIMIT 10;

#Weekly Trend
WITH weekly_prices AS (

SELECT

    YEAR(price_date) AS year,

    WEEK(price_date,1) AS week_number,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY

    YEAR(price_date),
    WEEK(price_date,1)

)

SELECT

    year,

    week_number,

    average_price,

    LAG(average_price)
    OVER(
        ORDER BY year, week_number
    ) AS previous_week,

    ROUND(
        average_price -
        LAG(average_price)
        OVER(
            ORDER BY year, week_number
        ),
    2) AS weekly_change

FROM weekly_prices;

#How does the average market price evolve as the weeks go by?
WITH weekly_prices AS (

SELECT

    YEAR(price_date) AS year,

    WEEK(price_date,1) AS week_number,

    ROUND(
        AVG(settlement_price),
        2
    ) AS average_price

FROM market_prices

GROUP BY

    YEAR(price_date),
    WEEK(price_date,1)

)

SELECT

    year,

    week_number,

    average_price,

    ROUND(

        AVG(average_price)

        OVER(

            ORDER BY year, week_number

            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW

        ),

    2) AS running_average

FROM weekly_prices;