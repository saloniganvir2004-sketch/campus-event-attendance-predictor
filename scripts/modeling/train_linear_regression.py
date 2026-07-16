import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

INPUT_FILE = Path("data/processed/events_features.csv")
MODEL_DIR = Path("data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Drop non-numeric / unused columns
X = df.drop(columns=["attendance_count", "event_name", "event_date", "start_time"])
X = X.astype(int)

y = df["attendance_count"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5

print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

joblib.dump(model, MODEL_DIR / "linear_regression.pkl")

print("Model saved successfully.")