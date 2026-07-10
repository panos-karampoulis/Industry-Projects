CREATE DATABASE energy_trading_db;

USE energy_trading_db;

CREATE TABLE traders (
    trader_id INT PRIMARY KEY AUTO_INCREMENT,
    trader_name VARCHAR(100) NOT NULL,
    desk VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE markets (
    market_id INT PRIMARY KEY AUTO_INCREMENT,
    market_name VARCHAR(100) NOT NULL,
    market_type VARCHAR(50)
);

CREATE TABLE assets (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50),
    capacity_mw DECIMAL(10,2)
);

CREATE TABLE trades (
    trade_id INT PRIMARY KEY AUTO_INCREMENT,
    
    trader_id INT,
    market_id INT,
    asset_id INT,
    
    trade_date DATE,
    
    volume_mwh DECIMAL(10,2),
    price DECIMAL(10,2),
    
    FOREIGN KEY (trader_id)
        REFERENCES traders(trader_id),
        
    FOREIGN KEY (market_id)
        REFERENCES markets(market_id),
        
    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)
);

CREATE TABLE market_prices (

    price_id INT PRIMARY KEY AUTO_INCREMENT,

    market_id INT,

    price_date DATE,

    settlement_price DECIMAL(10,2),

    FOREIGN KEY (market_id)
        REFERENCES markets(market_id)

);

ALTER TABLE trades
ADD COLUMN trade_type VARCHAR(10);

DESCRIBE trades;

ALTER TABLE trades
ADD COLUMN trade_timestamp DATETIME;

ALTER TABLE markets
ADD COLUMN country VARCHAR(50);

ALTER TABLE assets
ADD COLUMN renewable BOOLEAN;

CREATE TABLE generation (

    generation_id INT PRIMARY KEY AUTO_INCREMENT,

    asset_id INT,

    generation_timestamp DATETIME,

    generation_mwh DECIMAL(10,2),

    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)

);

ALTER TABLE market_prices
ADD COLUMN price_timestamp DATETIME;

ALTER TABLE market_prices
ADD COLUMN hour INT,
ADD COLUMN peak_type VARCHAR(20);