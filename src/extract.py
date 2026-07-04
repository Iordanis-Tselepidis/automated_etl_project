import requests
import json
from typing import Dict, Any, List


# ----------------------------
# CONFIG
# ----------------------------

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ERA5_URL = "https://archive-api.open-meteo.com/v1/era5"

CITIES = ["Berlin", "Paris", "London", "Rome", "Athens"]

START_DATE = "2021-01-01"
END_DATE = "2021-01-31"  # keep small for testing; expand later carefully

HOURLY_VARIABLES = "temperature_2m"


# ----------------------------
# STEP 1: GEOCODING
# ----------------------------

def get_coordinates(city: str) -> Dict[str, Any]:
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"No geocoding results found for {city}")

    result = data["results"][0]

    return {
        "city": city,
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country"),
    }


# ----------------------------
# STEP 2: WEATHER EXTRACTION
# ----------------------------

def fetch_historical_weather(lat: float, lon: float) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": HOURLY_VARIABLES,
        "timezone": "auto",
    }

    response = requests.get(ERA5_URL, params=params, timeout=60)
    response.raise_for_status()

    return response.json()


# ----------------------------
# STEP 3: PIPELINE
# ----------------------------

def run_pipeline() -> Dict[str, Any]:
    results = {}

    for city in CITIES:
        print(f"Processing {city}...")

        # 1. Get coordinates
        coords = get_coordinates(city)

        # 2. Fetch weather
        weather = fetch_historical_weather(
            coords["latitude"],
            coords["longitude"],
        )

        # 3. Store combined result
        results[city] = {
            "location": coords,
            "weather": weather,
        }

    return results


# ----------------------------
# STEP 4: SAVE OUTPUT
# ----------------------------

def save_to_file(data: Dict[str, Any], filename: str = "multi_city_weather.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved output to {filename}")


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    print("Starting ETL pipeline...\n")

    data = run_pipeline()

    save_to_file(data)

    print("\nDone.")
