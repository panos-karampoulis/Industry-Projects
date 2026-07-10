#DAILY REPORT
USE energy_trading_db;

DROP PROCEDURE IF EXISTS sp_daily_market_summary;

DELIMITER $$

CREATE PROCEDURE sp_daily_market_summary()

BEGIN

SELECT *

FROM vw_daily_market_summary

ORDER BY price_date;

END $$

DELIMITER ;

CALL sp_daily_market_summary();

###MONTHLY REPORT
DROP PROCEDURE IF EXISTS sp_monthly_market_summary;

DELIMITER $$

CREATE PROCEDURE sp_monthly_market_summary()

BEGIN

SELECT *

FROM vw_monthly_market_summary

ORDER BY

year,

month;

END $$

DELIMITER ;

CALL sp_monthly_market_summary();

######TRADER RANKING

DROP PROCEDURE IF EXISTS sp_trader_ranking;

DELIMITER $$

CREATE PROCEDURE sp_trader_ranking()

BEGIN

SELECT *

FROM vw_trader_performance

ORDER BY pnl DESC;

END $$

DELIMITER ;

#####STORED FUNCTION

USE energy_trading_db;

DROP FUNCTION IF EXISTS fn_trade_value;

DELIMITER $$

CREATE FUNCTION fn_trade_value(

    volume DECIMAL(10,2),

    price DECIMAL(10,2)

)

RETURNS DECIMAL(12,2)

DETERMINISTIC

BEGIN

RETURN volume * price;

END $$

DELIMITER ;

SELECT

trade_id,

fn_trade_value(volume_mwh,price)

FROM trades

LIMIT 20;