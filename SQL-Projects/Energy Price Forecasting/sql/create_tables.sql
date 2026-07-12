USE EnergyMarketForecasting;


CREATE TABLE energy_prices (

    id INT AUTO_INCREMENT PRIMARY KEY,

    Date DATE,

    Demand_MWh FLOAT,

    Wind_Generation_MWh FLOAT,

    Solar_Generation_MWh FLOAT,

    Gas_Price_EUR FLOAT,

    CO2_Price_EUR FLOAT,

    Temperature_C FLOAT,

    Electricity_Price_EUR FLOAT

);