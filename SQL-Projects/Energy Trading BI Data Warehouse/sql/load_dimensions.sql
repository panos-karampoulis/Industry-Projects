USE energy_dw;


INSERT INTO dim_trader

(
    trader_id,
    trader_name,
    desk,
    country
)

SELECT

    trader_id,
    trader_name,
    desk,
    country

FROM energy_trading_db.traders;

################ LOAD DIM-MARKET
INSERT INTO dim_market

(
    market_id,
    market_name,
    market_type,
    country
)

SELECT

    market_id,
    market_name,
    market_type,
    country

FROM energy_trading_db.markets;

#########LOAD DIM-ASSET
INSERT INTO dim_asset

(
    asset_id,
    asset_name,
    asset_type,
    renewable,
    capacity_mw
)

SELECT

    asset_id,
    asset_name,
    asset_type,
    renewable,
    capacity_mw

FROM energy_trading_db.assets;


SELECT *
FROM dim_asset;