def get_soil_health(lat, lon):
    return {
        "organic_matter": round(2.5 + lon / 1000, 1),
        "nitrogen": round(0.5 + lat / 1000, 1),
        "phosphorus": round(15 + lat / 100, 1),
        "potassium": round(120 + lon / 100, 1),
        "recommendations": [
            "Add compost for organic matter improvement",
            "Apply nitrogen-rich fertilizer during next planting",
        ],
    }
