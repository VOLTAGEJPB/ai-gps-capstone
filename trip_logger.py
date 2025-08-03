
import os
import json
from datetime import datetime
from typing import Tuple, Optional

TRIP_LOG_PATH = os.path.join(os.path.dirname(__file__), "trip_log.json")

def log_trip(start: Tuple[float, float], end: Tuple[float, float]):
    trip = {
        "start": start,
        "end": end,
        "timestamp": datetime.now().isoformat()
    }
    trips = []
    if os.path.exists(TRIP_LOG_PATH):
        with open(TRIP_LOG_PATH, "r") as f:
            trips = json.load(f)
    trips.append(trip)
    with open(TRIP_LOG_PATH, "w") as f:
        json.dump(trips, f, indent=2)

def suggest_better_route(start: Tuple[float, float], end: Tuple[float, float]) -> Optional[str]:
    if not os.path.exists(TRIP_LOG_PATH):
        return None
    with open(TRIP_LOG_PATH, "r") as f:
        trips = json.load(f)

    count = 0
    for trip in trips:
        if trip["start"] == start and trip["end"] == end:
            count += 1

    if count >= 2:
        return f"📌 You've taken this route {count} times. Consider checking traffic for shortcuts!"
    elif count == 1:
        return "📌 You’ve taken this route before. Want to try an alternate path?"
    return None
