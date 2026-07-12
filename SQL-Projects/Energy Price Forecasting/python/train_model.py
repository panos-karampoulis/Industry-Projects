import pandas as pd
import pymysql
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

connection = pymysql.connect(

    host="localhost",
    user="root",
    password="Econ12070",
    database="EnergyMarketForecasting"

)


query = """
SELECT *
FROM energy_prices;
"""


df = pd.read_sql(
    query,
    connection
)


connection.close()


print(df.head())

df = df.drop(
    columns=["id", "Date"]
)

X = df.drop(
    columns=["Electricity_Price_EUR"]
)


y = df["Electricity_Price_EUR"]


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)

model = RandomForestRegressor(

    n_estimators=200,
    random_state=42

)


model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)


mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)


r2 = r2_score(
    y_test,
    predictions
)


print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)


import matplotlib.pyplot as plt


results = pd.DataFrame({

    "Actual": y_test.values,

    "Predicted": predictions

})


plt.figure(figsize=(10,5))

plt.plot(
    results["Actual"],
    label="Actual Price"
)

plt.plot(
    results["Predicted"],
    label="Predicted Price"
)


plt.title(
    "Actual vs Predicted Electricity Price"
)

plt.xlabel(
    "Test Samples"
)

plt.ylabel(
    "€/MWh"
)


plt.legend()

plt.tight_layout()


plt.savefig(
    "charts/actual_vs_predicted.png"
)


plt.show()

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})


importance = importance.sort_values(
    by="Importance",
    ascending=False
)


print(importance)


import pickle
import os


os.makedirs(
    "models",
    exist_ok=True
)


with open(
    "models/energy_price_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print("Model saved successfully")
