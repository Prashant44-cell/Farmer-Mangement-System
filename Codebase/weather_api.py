import requests

def get_weather(city="Delhi"):
    API_KEY = "ccfceca6ac6c6f170a961f260287ab24"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    try:
        r = requests.get(url)
        data = r.json()
        if r.status_code == 200:
            return {
                "City": city,
                "Temperature": data["main"]["temp"],
                "Weather": data["weather"][0]["description"],
                "Humidity": data["main"]["humidity"],
                "Wind Speed": data["wind"]["speed"],
                "Pressure": data["main"]["pressure"],
            }
        return {"Error": data.get("message", "Unable to fetch data.")}
    except Exception as e:
        return {"Error": str(e)}

def get_rain_forecast(city="Delhi"):
    API_KEY = "ccfceca6ac6c6f170a961f260287ab24"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={API_KEY}&units=metric"
    try:
        r = requests.get(url)
        data = r.json()
        if r.status_code == 200:
            forecasts = {}
            for entry in data["list"]:
                date = entry["dt_txt"].split(" ")[0]
                rain = entry.get("rain", {}).get("3h", 0)
                forecasts.setdefault(date, []).append(rain)
                if len(forecasts) >= 3:
                    break
            return [
                {"date": d, "rainfall_mm": round(sum(vals) / len(vals), 1)}
                for d, vals in forecasts.items()
            ]
        return []
    except:
        return []
