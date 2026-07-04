import json
from typing import Dict, Any, List
import pandas as pd


# ----------------------------
# LOAD RAW DATA
# ----------------------------

def load_raw_data(path: str = "multi_city_weather.json") -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


# ----------------------------
# FLATTEN ONE CITY
# ----------------------------

def flatten_city(city: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    weather = payload["weather"]
    hourly = weather.get("hourly", {})

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    rows = []

    for t, temp in zip(times, temps):
        rows.append({
            "city": city,
            "time": t,
            "temperature_2m": temp
        })

    return rows


# ----------------------------
# TRANSFORM FULL DATASET
# ----------------------------

def transform_all(data: Dict[str, Any]) -> pd.DataFrame:
    all_rows = []

    for city, payload in data.items():
        rows = flatten_city(city, payload)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    # Convert time column to datetime (important for analytics)
    df["time"] = pd.to_datetime(df["time"])

    return df


# ----------------------------
# SAVE OUTPUTS
# ----------------------------

def save_outputs(df: pd.DataFrame):
    # Clean CSV (human readable)
    df.to_csv("clean_weather.csv", index=False)

    # Parquet (best for performance / big data)
    df.to_parquet("clean_weather.parquet", index=False)

    print("Saved:")
    print("- clean_weather.csv")
    print("- clean_weather.parquet")


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    print("Loading raw data...")

    raw = load_raw_data()

    print("Transforming...")

    df = transform_all(raw)

    print("\nPreview:")
    print(df.head())

    print("\nSaving outputs...")

    save_outputs(df)

    print("\nDone.")
