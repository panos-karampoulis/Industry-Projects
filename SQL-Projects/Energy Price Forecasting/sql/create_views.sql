USE EnergyMarketForecasting;


CREATE VIEW vw_daily_market_summary AS

SELECT

    Date,

    Demand_MWh,

    Wind_Generation_MWh,

    Solar_Generation_MWh,

    Electricity_Price_EUR

FROM energy_prices;


CREATE VIEW vw_price_drivers AS

SELECT

    Date,

    Electricity_Price_EUR,

    Demand_MWh,

    Gas_Price_EUR,

    CO2_Price_EUR,

    Wind_Generation_MWh,

    Solar_Generation_MWh

FROM energy_prices;

CREATE VIEW vw_renewable_impact AS

SELECT

    Date,

    (Wind_Generation_MWh + Solar_Generation_MWh)
    AS Renewable_Generation_MWh,

    Electricity_Price_EUR

FROM energy_prices;


SELECT *
FROM vw_price_drivers
LIMIT 5;