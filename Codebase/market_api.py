import requests
from utils import safe_get_secret

def get_crop_prices(crop="wheat"):
    API_KEY = safe_get_secret("AMBEEDATA_API_KEY", "YOUR_AMBEEDATA_API_KEY")
    if not API_KEY or API_KEY.startswith("YOUR_"):
        return {"price": 4500, "unit": "INR/Quintal"}
    url = f"https://api.ambeedata.com/market/v2/prices/{crop}"
    headers = {"x-api-key": API_KEY}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return {"price": 4500, "unit": "INR/Quintal"}
    except:
        return {"price": 4500, "unit": "INR/Quintal"}
