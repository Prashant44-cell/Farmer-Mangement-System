import requests
from datetime import datetime
from utils import safe_get_secret

def get_agri_news():
    API_KEY = safe_get_secret("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")
    if not API_KEY or API_KEY.startswith("YOUR_"):
        return [
            {
                "title": "Agricultural News API Not Configured",
                "url": "#",
                "source": "System",
                "date": datetime.now().strftime("%d %b %Y"),
            },
            {
                "title": "Please add your NewsAPI key to secrets",
                "url": "https://newsapi.org/",
                "source": "NewsAPI",
                "date": datetime.now().strftime("%d %b %Y"),
            },
        ]
    url = f"https://newsapi.org/v2/everything?q=agriculture&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        arts = r.json().get("articles", [])[:3]
        news = []
        for a in arts:
            date = datetime.strptime(a["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                "%d %b %Y"
            )
            news.append(
                {
                    "title": a.get("title", "No title"),
                    "url": a.get("url", "#"),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "date": date,
                }
            )
        return news
    except:
        return []
