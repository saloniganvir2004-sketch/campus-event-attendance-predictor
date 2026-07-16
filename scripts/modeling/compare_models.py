import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

INPUT_FILE = Path("data/processed/events_features.csv")

df = pd.read_csv(INPUT_FILE)

X = df.drop(columns=["attendance_count", "event_name", "event_date", "start_time"])
X = X.astype(int)

y = df["attendance_count"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
}

results = []

for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    results.append({
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2)
    })

results = pd.DataFrame(results)

print(results)

best = results.sort_values("RMSE").iloc[0]

print("\nBest Model:")
print(best)