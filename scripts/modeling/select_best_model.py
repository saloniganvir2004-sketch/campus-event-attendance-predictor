import joblib
import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

DATA = Path("data/processed/events_processed.csv")
MODEL_DIR = Path("data/models")

df = pd.read_csv(DATA)

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

categorical = [
    "category_name",
    "day_of_week",
    "weather_condition",
]

numeric = [
    "venue_capacity",
    "is_weekend",
    "is_holiday",
    "month",
    "day",
    "start_hour",
]

preprocessor = ColumnTransformer(
    [
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical,
        ),
        (
            "num",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                ]
            ),
            numeric,
        ),
    ]
)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    ),
}

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

best_name = None
best_score = float("inf")
best_pipeline = None

for name, model in models.items():

    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train, y_train)

    prediction = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        prediction,
    )

    print(name, "MAE:", round(mae, 2))

    if mae < best_score:
        best_score = mae
        best_name = name
        best_pipeline = pipeline

joblib.dump(
    best_pipeline,
    MODEL_DIR / "best_model.pkl",
)

print("\nBest Model:", best_name)