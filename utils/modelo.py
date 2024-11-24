import pickle
import streamlit as st

@st.cache_data
def obtener_modelo():
    return pickle.load(open("model.sav", "rb"))