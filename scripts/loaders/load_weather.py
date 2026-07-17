import sqlite3
import pandas as pd
from pathlib import Path

DATABASE = Path("database/database.db")
WEATHER_FILE = Path("data/staging/weather_staging.csv")

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

weather_df = pd.read_csv(WEATHER_FILE)

for _, row in weather_df.iterrows():
    cursor.execute(
        """
        INSERT OR REPLACE INTO weather (
            event_date,
            weather_condition,
            temperature,
            precipitation
)
VALUES (?, ?, ?, ?)
        """,
        (
            row["event_date"],
            str(row["weather_code"]),
            float(
                (row["temperature_max"] + row["temperature_min"]) / 2
            ),
            float(row["precipitation"]),
        )
    )

conn.commit()
conn.close()

print("Weather data loaded successfully.")