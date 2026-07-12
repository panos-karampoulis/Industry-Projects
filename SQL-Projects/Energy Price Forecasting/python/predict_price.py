import pandas as pd
import pickle


# Load trained model

with open(
    "models/energy_price_model.pkl",
    "rb"
) as file:

    model = pickle.load(file)


print("Model loaded successfully")


# Example future conditions

new_data = pd.DataFrame({

    "Demand_MWh": [36000],

    "Wind_Generation_MWh": [7500],

    "Solar_Generation_MWh": [3000],

    "Gas_Price_EUR": [45],

    "CO2_Price_EUR": [85],

    "Temperature_C": [20]

})


# Prediction

prediction = model.predict(
    new_data
)


print(
    f"Predicted Electricity Price: {prediction[0]:.2f} €/MWh"
)