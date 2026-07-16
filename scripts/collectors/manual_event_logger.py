import pandas as pd
from pathlib import Path

STAGING_DIR = Path("data/staging")
STAGING_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = STAGING_DIR / "events_staging.csv"

columns = [
    "event_name",
    "category",
    "event_date",
    "day_of_week",
    "start_time",
    "venue_capacity",
    "weather_condition",
    "is_weekend",
    "is_holiday",
    "attendance_count"
]

if not OUTPUT_FILE.exists():
    pd.DataFrame(columns=columns).to_csv(OUTPUT_FILE, index=False)

print(f"Staging file ready: {OUTPUT_FILE}")