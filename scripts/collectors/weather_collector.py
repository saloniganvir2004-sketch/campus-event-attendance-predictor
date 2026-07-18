import psycopg2
import pandas as pd
from pathlib import Path

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_events",
    "user": "user",
    "password": "password",
}

DATA_FILE = Path("data/staging/weather_staging.csv")

def load_weather_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    weather_df = pd.read_csv(DATA_FILE)

    for _, row in weather_df.iterrows():
        cursor.execute(
            """
            INSERT INTO weather (
                event_date,
                weather_code,
                temperature_avg,
                precipitation
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (event_date) DO UPDATE SET
                weather_code = EXCLUDED.weather_code,
                temperature_avg = EXCLUDED.temperature_avg,
                precipitation = EXCLUDED.precipitation;
            """,
            (
                row["event_date"],
                str(row["weather_condition"]),
                float((row["temperature_max"] + row["temperature_min"]) / 2),
                float(row["precipitation"]),
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_weather_data()
    print("Weather data loaded successfully.")