USE energy_dw;


INSERT INTO dim_date

(
date_key,
full_date,
day_number,
month_number,
month_name,
quarter_number,
year_number,
week_number,
weekday_name
)

SELECT

DATE_FORMAT(price_date,'%Y%m%d'),

price_date,

DAY(price_date),

MONTH(price_date),

MONTHNAME(price_date),

QUARTER(price_date),

YEAR(price_date),

WEEK(price_date,1),

DAYNAME(price_date)

FROM

(
SELECT DISTINCT

price_date

FROM energy_trading_db.market_prices

) dates;


SELECT *

FROM dim_date

LIMIT 10;