import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_trip_duration(start_location, end_location):
    """
    Returns estimated driving time in minutes using real-time traffic data.
    """
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": start_location,
        "destinations": end_location,
        "departure_time": "now",  # real-time traffic
        "traffic_model": "best_guess",
        "mode": "driving",
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        if response.status_code != 200 or data["status"] != "OK":
            print("❌ Error with Google Maps API:", data)
            return None

        element = data["rows"][0]["elements"][0]
        if element["status"] != "OK":
            print("❌ Location error:", element["status"])
            return None

        # Duration in traffic (seconds) → minutes
        duration_seconds = element["duration_in_traffic"]["value"]
        return duration_seconds // 60

    except Exception as e:
        print("❌ Exception in get_trip_duration:", e)
        return None
