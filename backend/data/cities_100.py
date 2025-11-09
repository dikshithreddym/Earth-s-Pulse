"""
List of 100 major world cities with approximate lat/lng coordinates.
Used by the seed script to populate one mood point per city (distributed globally).
"""

CITIES_100 = [
    {"lat": 40.7128, "lng": -74.0060, "name": "New York, USA"},
    {"lat": 34.0522, "lng": -118.2437, "name": "Los Angeles, USA"},
    {"lat": 41.8781, "lng": -87.6298, "name": "Chicago, USA"},
    {"lat": 29.7604, "lng": -95.3698, "name": "Houston, USA"},
    {"lat": 33.4484, "lng": -112.0740, "name": "Phoenix, USA"},
    {"lat": 39.9526, "lng": -75.1652, "name": "Philadelphia, USA"},
    {"lat": 29.4241, "lng": -98.4936, "name": "San Antonio, USA"},
    {"lat": 32.7157, "lng": -117.1611, "name": "San Diego, USA"},
    {"lat": 32.7767, "lng": -96.7970, "name": "Dallas, USA"},
    {"lat": 37.3382, "lng": -121.8863, "name": "San Jose, USA"},

    {"lat": 43.6532, "lng": -79.3832, "name": "Toronto, Canada"},
    {"lat": 45.5017, "lng": -73.5673, "name": "Montreal, Canada"},
    {"lat": 49.2827, "lng": -123.1207, "name": "Vancouver, Canada"},
    {"lat": 19.4326, "lng": -99.1332, "name": "Mexico City, Mexico"},
    {"lat": 20.6597, "lng": -103.3496, "name": "Guadalajara, Mexico"},

    {"lat": -34.6037, "lng": -58.3816, "name": "Buenos Aires, Argentina"},
    {"lat": -23.5505, "lng": -46.6333, "name": "São Paulo, Brazil"},
    {"lat": -22.9068, "lng": -43.1729, "name": "Rio de Janeiro, Brazil"},
    {"lat": -12.0464, "lng": -77.0428, "name": "Lima, Peru"},
    {"lat": -33.4489, "lng": -70.6693, "name": "Santiago, Chile"},

    {"lat": 4.7110, "lng": -74.0721, "name": "Bogotá, Colombia"},
    {"lat": 10.4806, "lng": -66.9036, "name": "Caracas, Venezuela"},
    {"lat": 8.9824, "lng": -79.5199, "name": "Panama City, Panama"},
    {"lat": -0.1807, "lng": -78.4678, "name": "Quito, Ecuador"},
    {"lat": -12.0433, "lng": -77.0283, "name": "Callao/Lima Port, Peru"},

    {"lat": 25.2048, "lng": 55.2708, "name": "Dubai, UAE"},
    {"lat": 24.7136, "lng": 46.6753, "name": "Riyadh, Saudi Arabia"},
    {"lat": 41.0082, "lng": 28.9784, "name": "Istanbul, Turkey"},
    {"lat": 51.5074, "lng": -0.1278, "name": "London, UK"},
    {"lat": 48.8566, "lng": 2.3522, "name": "Paris, France"},

    {"lat": 52.5200, "lng": 13.4050, "name": "Berlin, Germany"},
    {"lat": 41.9028, "lng": 12.4964, "name": "Rome, Italy"},
    {"lat": 40.4168, "lng": -3.7038, "name": "Madrid, Spain"},
    {"lat": 55.7558, "lng": 37.6173, "name": "Moscow, Russia"},
    {"lat": 59.9343, "lng": 30.3351, "name": "Saint Petersburg, Russia"},

    {"lat": 50.0755, "lng": 14.4378, "name": "Prague, Czechia"},
    {"lat": 48.2082, "lng": 16.3738, "name": "Vienna, Austria"},
    {"lat": 47.4979, "lng": 19.0402, "name": "Budapest, Hungary"},
    {"lat": 60.1699, "lng": 24.9384, "name": "Helsinki, Finland"},
    {"lat": 59.3293, "lng": 18.0686, "name": "Stockholm, Sweden"},

    {"lat": 59.9139, "lng": 10.7522, "name": "Oslo, Norway"},
    {"lat": 55.6761, "lng": 12.5683, "name": "Copenhagen, Denmark"},
    {"lat": 64.1466, "lng": -21.9426, "name": "Reykjavik, Iceland"},
    {"lat": 35.6895, "lng": 139.6917, "name": "Tokyo, Japan"},
    {"lat": 34.6937, "lng": 135.5023, "name": "Osaka, Japan"},

    {"lat": 37.5665, "lng": 126.9780, "name": "Seoul, South Korea"},
    {"lat": 31.2304, "lng": 121.4737, "name": "Shanghai, China"},
    {"lat": 39.9042, "lng": 116.4074, "name": "Beijing, China"},
    {"lat": 22.3964, "lng": 114.1095, "name": "Hong Kong"},
    {"lat": 1.3521, "lng": 103.8198, "name": "Singapore"},

    {"lat": 13.7563, "lng": 100.5018, "name": "Bangkok, Thailand"},
    {"lat": 3.1390, "lng": 101.6869, "name": "Kuala Lumpur, Malaysia"},
    {"lat": -6.2088, "lng": 106.8456, "name": "Jakarta, Indonesia"},
    {"lat": 14.5995, "lng": 120.9842, "name": "Manila, Philippines"},
    {"lat": 21.0278, "lng": 105.8342, "name": "Hanoi, Vietnam"},

    {"lat": 10.8231, "lng": 106.6297, "name": "Ho Chi Minh City, Vietnam"},
    {"lat": 28.7041, "lng": 77.1025, "name": "Delhi, India"},
    {"lat": 19.0760, "lng": 72.8777, "name": "Mumbai, India"},
    {"lat": 12.9716, "lng": 77.5946, "name": "Bengaluru, India"},
    {"lat": 13.0827, "lng": 80.2707, "name": "Chennai, India"},

    {"lat": 23.8103, "lng": 90.4125, "name": "Dhaka, Bangladesh"},
    {"lat": 24.8607, "lng": 67.0011, "name": "Karachi, Pakistan"},
    {"lat": 33.6844, "lng": 73.0479, "name": "Islamabad, Pakistan"},
    {"lat": 31.5204, "lng": 74.3587, "name": "Lahore, Pakistan"},
    {"lat": 27.7172, "lng": 85.3240, "name": "Kathmandu, Nepal"},

    {"lat": 6.9271, "lng": 79.8612, "name": "Colombo, Sri Lanka"},
    {"lat": 32.0853, "lng": 34.7818, "name": "Tel Aviv, Israel"},
    {"lat": 31.7683, "lng": 35.2137, "name": "Jerusalem, Israel"},
    {"lat": 30.0444, "lng": 31.2357, "name": "Cairo, Egypt"},
    {"lat": -1.2864, "lng": 36.8172, "name": "Nairobi, Kenya"},

    {"lat": -26.2041, "lng": 28.0473, "name": "Johannesburg, South Africa"},
    {"lat": -33.9249, "lng": 18.4241, "name": "Cape Town, South Africa"},
    {"lat": 6.5244, "lng": 3.3792, "name": "Lagos, Nigeria"},
    {"lat": 5.6037, "lng": -0.1870, "name": "Accra, Ghana"},
    {"lat": 33.5731, "lng": -7.5898, "name": "Casablanca, Morocco"},

    {"lat": 36.7538, "lng": 3.0588, "name": "Algiers, Algeria"},
    {"lat": 36.8065, "lng": 10.1815, "name": "Tunis, Tunisia"},
    {"lat": 9.0054, "lng": 38.7636, "name": "Addis Ababa, Ethiopia"},
    {"lat": 0.3476, "lng": 32.5825, "name": "Kampala, Uganda"},
    {"lat": -6.7924, "lng": 39.2083, "name": "Dar es Salaam, Tanzania"},

    {"lat": -37.8136, "lng": 144.9631, "name": "Melbourne, Australia"},
    {"lat": -33.8688, "lng": 151.2093, "name": "Sydney, Australia"},
    {"lat": -27.4698, "lng": 153.0251, "name": "Brisbane, Australia"},
    {"lat": -31.9523, "lng": 115.8613, "name": "Perth, Australia"},
    {"lat": -36.8485, "lng": 174.7633, "name": "Auckland, New Zealand"},

    {"lat": -41.2865, "lng": 174.7762, "name": "Wellington, New Zealand"},
    {"lat": 41.3851, "lng": 2.1734, "name": "Barcelona, Spain"},
    {"lat": 52.3676, "lng": 4.9041, "name": "Amsterdam, Netherlands"},
    {"lat": 50.1109, "lng": 8.6821, "name": "Frankfurt, Germany"},
    {"lat": 53.5511, "lng": 9.9937, "name": "Hamburg, Germany"},

    {"lat": 39.4699, "lng": -0.3763, "name": "Valencia, Spain"},
    {"lat": 55.8642, "lng": -4.2518, "name": "Glasgow, UK"},
    {"lat": 55.9533, "lng": -3.1883, "name": "Edinburgh, UK"},
    {"lat": 41.1579, "lng": -8.6291, "name": "Porto, Portugal"},
    {"lat": 45.8150, "lng": 15.9819, "name": "Zagreb, Croatia"},

    {"lat": 42.6977, "lng": 23.3219, "name": "Sofia, Bulgaria"},
    {"lat": 44.7866, "lng": 20.4489, "name": "Belgrade, Serbia"},
    {"lat": 43.8563, "lng": 18.4131, "name": "Sarajevo, Bosnia & Herzegovina"},
    {"lat": 59.4370, "lng": 24.7536, "name": "Tallinn, Estonia"},
    {"lat": 54.6872, "lng": 25.2797, "name": "Vilnius, Lithuania"},
]
