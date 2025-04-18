import streamlit as st
from services.ollama_phi3 import suggest

def display():
    st.header("Farmer Registration")

    with st.form("farmer_form"):
        name = st.text_input("Name")
        location = st.text_input("Location")
        crop = st.text_input("Crop Type", value=suggest("Crop"))
        submitted = st.form_submit_button("Save Record")

        if submitted:
            st.success("Farmer record saved!")
