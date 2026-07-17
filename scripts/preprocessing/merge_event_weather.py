import sqlite3
import pandas as pd
from pathlib import Path

DATABASE = Path("database/database.db")
OUTPUT_FILE = Path("data/processed/events_with_weather.csv")

conn = sqlite3.connect(DATABASE)

query = """
SELECT
    e.event_id,
    e.event_name,
    e.event_date,
    e.start_time,
    e.day_of_week,
    e.venue_capacity,
    e.is_weekend,
    e.is_holiday,
    c.category_name,
    a.attendance_count,
    w.weather_condition,
    w.temperature,
    w.precipitation
FROM events e
LEFT JOIN categories c
    ON e.category_id = c.category_id
LEFT JOIN attendance_logs a
    ON e.event_id = a.event_id
LEFT JOIN weather w
    ON e.event_date = w.event_date;
"""

df = pd.read_sql_query(query, conn)

conn.close()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Merged dataset created successfully.")
print(df.head())