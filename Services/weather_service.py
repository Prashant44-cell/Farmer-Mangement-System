import requests
import streamlit as st
from config import OPENWEATHER_API_KEY, WEATHER_BASE_URL

def get_weather_card(city):
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    response = requests.get(WEATHER_BASE_URL, params=params).json()

    if response.get("cod") == 200:
        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        wind = response["wind"]["speed"]

        st.markdown(f"""
            <div style="background: rgba(0,0,0,0.4); padding: 20px; border-radius: 20px; color: white; backdrop-filter: blur(10px);">
                <h2>{city}</h2>
                <p><b>Weather:</b> {weather}</p>
                <p><b>Temperature:</b> {temp} °C</p>
                <p><b>Humidity:</b> {humidity}%</p>
                <p><b>Wind Speed:</b> {wind} m/s</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("City not found or API error.")
