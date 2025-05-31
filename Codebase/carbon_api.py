import requests
from utils import safe_get_secret

def get_carbon_footprint(fertilizer_kg):
    API_KEY = safe_get_secret("CLIMATIQ_API_KEY", "YOUR_CLIMATIQ_API_KEY")
    if not API_KEY or API_KEY.startswith("YOUR_"):
        return 4.8 * fertilizer_kg
    url = "https://beta3.api.climatiq.io/estimate"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "emission_factor": {
            "activity_id": "chemicals_fertilizers_synthetic_nitrogen_production",
            "data_version": "^3",
        },
        "parameters": {"amount": fertilizer_kg, "amount_unit": "kg"},
    }
    try:
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            return r.json().get("co2e", 4.8 * fertilizer_kg)
        return 4.8 * fertilizer_kg
    except:
        return 4.8 * fertilizer_kg
