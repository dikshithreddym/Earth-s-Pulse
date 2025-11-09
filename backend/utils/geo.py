from __future__ import annotations
from math import radians, sin, cos, asin, sqrt
from typing import Tuple, Optional, Dict, Any, List
from data.cities_200 import CITIES_200

def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c

def nearest_city(lat: float, lng: float, within_km: float = 100) -> Optional[Dict[str, Any]]:
    best = None
    best_d = 1e9
    for c in CITIES_200:
        d = _haversine(lat, lng, c["lat"], c["lng"])
        if d < best_d:
            best = c
            best_d = d
    if best and best_d <= within_km:
        return {**best, "distance_km": round(best_d, 1)}
    return None