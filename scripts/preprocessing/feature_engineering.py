import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/processed/events_processed.csv")
OUTPUT_FILE = Path("data/processed/events_features.csv")

df = pd.read_csv(INPUT_FILE)

# Convert date
df["event_date"] = pd.to_datetime(df["event_date"])

# Date features
df["month"] = df["event_date"].dt.month
df["day"] = df["event_date"].dt.day

# Time feature
df["start_hour"] = df["start_time"].str.split(":").str[0].astype(int)

# One-hot encoding
df = pd.get_dummies(
    df,
    columns=[
        "category_name",
        "day_of_week",
        "weather_condition"
    ],
    drop_first=False
)

df.to_csv(OUTPUT_FILE, index=False)

print("Feature dataset created successfully!")
print(df.head())