CREATE DATABASE energy_dw;

USE energy_dw;

CREATE TABLE dim_trader (

    trader_key INT AUTO_INCREMENT PRIMARY KEY,

    trader_id INT,

    trader_name VARCHAR(100),

    desk VARCHAR(100),

    country VARCHAR(50)

);

CREATE TABLE dim_market (

    market_key INT AUTO_INCREMENT PRIMARY KEY,

    market_id INT,

    market_name VARCHAR(100),

    market_type VARCHAR(50),

    country VARCHAR(50)

);

CREATE TABLE dim_asset (

    asset_key INT AUTO_INCREMENT PRIMARY KEY,

    asset_id INT,

    asset_name VARCHAR(100),

    asset_type VARCHAR(50),

    renewable BOOLEAN,

    capacity_mw DECIMAL(10,2)

);


CREATE TABLE dim_date (

    date_key INT PRIMARY KEY,

    full_date DATE,

    day_number INT,

    month_number INT,

    month_name VARCHAR(20),

    quarter_number INT,

    year_number INT,

    week_number INT,

    weekday_name VARCHAR(20)

);


CREATE TABLE fact_trades (

    trade_key INT AUTO_INCREMENT PRIMARY KEY,

    trader_key INT,

    market_key INT,

    asset_key INT,

    date_key INT,

    volume_mwh DECIMAL(10,2),

    trade_price DECIMAL(10,2),

    trade_value DECIMAL(12,2),

    trade_type VARCHAR(10)

);