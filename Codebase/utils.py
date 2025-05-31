import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

def safe_get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except StreamlitSecretNotFoundError:
        return default
    except Exception:
        return default
