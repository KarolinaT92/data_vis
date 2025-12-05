"""
Generate city_coordinates.csv using OpenStreetMap geocoder (Nominatim)
Run ONCE on a machine with working internet.
"""

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
from pathlib import Path

# === PATHS ===
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "superstore_dataset" / "cleaned_Superstore.csv"
OUTPUT_PATH = BASE_DIR / "shared" / "city_coordinates.csv"

print(f"Loading data from: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, parse_dates=["Order Date"])
cities = df[["City", "State"]].drop_duplicates().reset_index(drop=True)

if OUTPUT_PATH.exists():
    existing = pd.read_csv(OUTPUT_PATH)
    geocoded = existing[["City", "State"]]
    merged = cities.merge(geocoded, on=["City", "State"], how="left", indicator=True)
    to_geocode = merged[merged["_merge"] == "left_only"][["City", "State"]]
    results = existing.copy()
    print(f"Resuming — {len(to_geocode)} cities left to geocode.")
else:
    to_geocode = cities.copy()
    results = pd.DataFrame(columns=["City", "State", "lat", "lon"])
    print(f"Fresh geocoding — {len(to_geocode)} cities total.")

# === Geocoder ===
geolocator = Nominatim(user_agent="superstore_customer_map")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

success, fail = 0, 0

for i, row in to_geocode.iterrows():
    city = row["City"]
    state = row["State"]

    query = f"{city}, {state}, USA"
    try:
        location = geocode(query)

        if location:
            results = pd.concat([
                results,
                pd.DataFrame([{
                    "City": city,
                    "State": state,
                    "lat": location.latitude,
                    "lon": location.longitude
                }])
            ], ignore_index=True)
            success += 1
            print(f"[OK] {city}, {state} → {location.latitude:.3f}, {location.longitude:.3f}")
        else:
            fail += 1
            print(f"[NO MATCH] {query}")

    except Exception as e:
        fail += 1
        print(f"[ERROR] {query} → {e}")


    if (success + fail) % 10 == 0:
        results.drop_duplicates(subset=["City", "State"]).to_csv(OUTPUT_PATH, index=False)

    time.sleep(1)

results.drop_duplicates(subset=["City", "State"]).to_csv(OUTPUT_PATH, index=False)

print("=== DONE ===")
print(f"Total geocoded: {success}")
print(f"Failed: {fail}")
print(f"Saved to: {OUTPUT_PATH}")
