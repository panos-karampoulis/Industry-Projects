#Which was the average electricity price per month?
SELECT
    MONTH(price_date) AS month,
    ROUND(AVG(settlement_price),2) AS avg_price
FROM market_prices
GROUP BY MONTH(price_date)
ORDER BY month;

#which months had the biggest price extremes?
SELECT
    MONTH(price_date) AS month,
    ROUND(MIN(settlement_price),2) AS min_price,
    ROUND(MAX(settlement_price),2) AS max_price
FROM market_prices
GROUP BY MONTH(price_date)
ORDER BY month;

#how much more expensive are the peak hours?
SELECT
    peak_type,
    COUNT(*) AS hours,
    ROUND(AVG(settlement_price),2) AS avg_price
FROM market_prices
GROUP BY peak_type;

#which hours were the most expensive in the market?
SELECT
    price_timestamp,
    settlement_price
FROM market_prices
ORDER BY settlement_price DESC
LIMIT 10;