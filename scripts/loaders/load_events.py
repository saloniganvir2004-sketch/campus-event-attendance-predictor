import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("database/database.db")
CSV_PATH = Path("data/staging/events_staging.csv")

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)

categories = {}

for category in df["category"].dropna().unique():
    conn.execute(
        "INSERT OR IGNORE INTO categories(category_name) VALUES (?)",
        (category,)
    )

conn.commit()

rows = conn.execute(
    "SELECT category_id, category_name FROM categories"
).fetchall()

for category_id, category_name in rows:
    categories[category_name] = category_id

for _, row in df.iterrows():

    weather = conn.execute(
        """
        INSERT OR IGNORE INTO weather
        (event_date, weather_condition)
        VALUES (?, ?)
        """,
        (
            row["event_date"],
            row["weather_condition"]
        )
    )

    conn.commit()

    weather_id = conn.execute(
        """
        SELECT weather_id
        FROM weather
        WHERE event_date = ?
        """,
        (row["event_date"],)
    ).fetchone()[0]

    conn.execute(
        """
        INSERT INTO events
        (
            event_name,
            category_id,
            event_date,
            day_of_week,
            start_time,
            venue_capacity,
            is_weekend,
            is_holiday
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["event_name"],
            categories[row["category"]],
            row["event_date"],
            row["day_of_week"],
            row["start_time"],
            int(row["venue_capacity"]),
            int(row["is_weekend"]),
            int(row["is_holiday"])
        )
    )

    event_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    conn.execute(
        """
        INSERT INTO attendance_logs
        (
            event_id,
            weather_id,
            attendance_count
        )
        VALUES (?, ?, ?)
        """,
        (
            event_id,
            weather_id,
            int(row["attendance_count"])
        )
    )

conn.commit()
conn.close()

print("Data loaded successfully.")