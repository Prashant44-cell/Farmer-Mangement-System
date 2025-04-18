import streamlit as st
from services.weather_service import get_weather_card

def display():
    st.markdown("### Weather Dashboard", unsafe_allow_html=True)
    city = st.selectbox("Select City", ["Mumbai", "Delhi", "Kolkata", "Chennai", "Bengaluru", "Lucknow"])
    
    if city:
        get_weather_card(city)
