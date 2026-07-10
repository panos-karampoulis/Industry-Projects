USE energy_dw;


INSERT INTO fact_trades

(

trader_key,

market_key,

asset_key,

date_key,

volume_mwh,

trade_price,

trade_value,

trade_type

)


SELECT


dt.trader_key,

dm.market_key,

da.asset_key,


DATE_FORMAT(tr.trade_date,'%Y%m%d'),


tr.volume_mwh,


tr.price,


tr.volume_mwh * tr.price,


tr.trade_type



FROM energy_trading_db.trades tr



JOIN dim_trader dt

ON tr.trader_id = dt.trader_id



JOIN dim_market dm

ON tr.market_id = dm.market_id



JOIN dim_asset da

ON tr.asset_id = da.asset_id;

