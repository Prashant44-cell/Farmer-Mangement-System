import streamlit as st
import pandas as pd
import os

def display():
    st.header("Upload CSV Folder")
    uploaded_files = st.file_uploader("Upload multiple CSVs", type="csv", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            df = pd.read_csv(file)
            st.subheader(file.name)
            st.dataframe(df)
