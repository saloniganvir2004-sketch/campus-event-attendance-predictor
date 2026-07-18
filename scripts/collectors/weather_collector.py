import requests
import pandas as pd
from pathlib import Path

WEATHER_CODES = {
    0: "Clear",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    80: "Rain Showers",
    81: "Heavy Showers",
    82: "Violent Showers",
    95: "Thunderstorm",
}


DATA_FILE = Path("data/staging/weather_staging.csv")

def collect_weather_data():
    """
    Collects historical weather data for a given location and date range using the Open-Meteo API,
    and saves it to data/staging/weather_staging.csv.
    """
    # Set your location and date range here
    latitude = 19.0760   # Example: Mumbai
    longitude = 72.8777
    start_date = "2025-07-01"
    end_date = "2025-08-15"
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Asia%2FKolkata"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Prepare DataFrame
    df = pd.DataFrame({
        "event_date": data["daily"]["time"],
        "weather_condition": [
            WEATHER_CODES.get(code, "Unknown")
            for code in data["daily"]["weathercode"]
        ],
        "temperature_max": data["daily"]["temperature_2m_max"],
        "temperature_min": data["daily"]["temperature_2m_min"],
        "precipitation": data["daily"]["precipitation_sum"],
    })
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_FILE, index=False)

if __name__ == "__main__":
    collect_weather_data()
    print(f"Weather data collected and saved to {DATA_FILE}.")