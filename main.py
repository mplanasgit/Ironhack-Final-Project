import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import base64

st.set_page_config(
     page_title="PM10 in Europe",
     page_icon="🌫️",
     layout="wide",
     initial_sidebar_state="expanded",
 )

st.title("Plan your trip: Forecasting seasonal pollutants")
st.write("                      *Ironhack Final Project*")
st.write("")
st.write("                      by **Marc Planas Marquès**")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local("./images/balkans_pollution_image.jpg") 