import streamlit as st
import src.tools.style as sty

st.set_page_config(
     page_title="PM10 in Europe",
     page_icon="🌫️",
     layout="wide",
     initial_sidebar_state="expanded",
 )

st.title("Plan your trip: Forecasting seasonal pollutants")
st.write("*Ironhack Final Project*")
st.write("")
st.write("by **Marc Planas Marquès**")

sty.add_bg_from_local("./images/balkans_pollution_image.jpg") 