import requests
import pandas as pd
from pathlib import Path

LATITUDE = 28.5445
LONGITUDE = 77.3332

START_DATE = "2025-07-01"
END_DATE = "2025-08-31"

OUTPUT_DIR = Path("data/staging")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "weather_staging.csv"

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    f"&start_date={START_DATE}"
    f"&end_date={END_DATE}"
    "&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_sum,weather_code"
    "&timezone=auto"
)

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()["daily"]

weather_df = pd.DataFrame({
    "event_date": data["time"],
    "temperature_max": data["temperature_2m_max"],
    "temperature_min": data["temperature_2m_min"],
    "precipitation": data["precipitation_sum"],
    "weather_code": data["weather_code"],
})

weather_df.to_csv(OUTPUT_FILE, index=False)

print("Weather staging file created successfully.")
print(weather_df.head())