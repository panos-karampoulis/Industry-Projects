USE energy_trading_db;

SELECT *
FROM traders;

SELECT COUNT(*)
FROM market_prices;

SELECT *
FROM market_prices
LIMIT 10;

SELECT *
FROM market_prices
WHERE price_timestamp IS NULL
   OR settlement_price IS NULL;
SET SQL_SAFE_UPDATES = 0;
   
UPDATE market_prices
SET price_date = DATE(price_timestamp);
SELECT 
    price_timestamp,
    price_date
FROM market_prices
LIMIT 10;

SELECT 
    price_timestamp,
    price_date,
    DATE(price_timestamp) AS extracted_date
FROM market_prices
LIMIT 10;

DESCRIBE market_prices;