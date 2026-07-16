import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("database/database.db")
OUTPUT_PATH = Path("data/processed/events_processed.csv")

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    e.event_name,
    c.category_name,
    e.event_date,
    e.day_of_week,
    e.start_time,
    e.venue_capacity,
    w.weather_condition,
    e.is_weekend,
    e.is_holiday,
    a.attendance_count
FROM events e
JOIN categories c
ON e.category_id = c.category_id
JOIN attendance_logs a
ON e.event_id = a.event_id
JOIN weather w
ON a.weather_id = w.weather_id
"""

df = pd.read_sql(query, conn)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

conn.close()

print("Processed dataset created successfully.")
print(df.head())