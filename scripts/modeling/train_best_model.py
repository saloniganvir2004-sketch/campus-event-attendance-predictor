import joblib
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path("data/processed/events_processed.csv")
MODEL_DIR = Path("data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df["event_date"] = pd.to_datetime(df["event_date"])
df["month"] = df["event_date"].dt.month
df["day"] = df["event_date"].dt.day
df["start_hour"] = df["start_time"].str.split(":").str[0].astype(int)

X = df[
    [
        "category_name",
        "day_of_week",
        "weather_condition",
        "venue_capacity",
        "is_weekend",
        "is_holiday",
        "month",
        "day",
        "start_hour",
    ]
]

y = df["attendance_count"]

categorical_features = [
    "category_name",
    "day_of_week",
    "weather_condition",
]

numeric_features = [
    "venue_capacity",
    "is_weekend",
    "is_holiday",
    "month",
    "day",
    "start_hour",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical_features,
        ),
        (
            "num",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                ]
            ),
            numeric_features,
        ),
    ]
)

pipeline = Pipeline(
    [
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
            ),
        ),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5

print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

joblib.dump(pipeline, MODEL_DIR / "best_model.pkl")

print("Best model saved successfully.")