# Libraries
import streamlit as st
import src.tools.style as sty
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
     page_title="PM10 in Europe",
     page_icon="🌫️",
     layout="wide",
     initial_sidebar_state="expanded",
 )
# Adding background image
sty.add_bg_from_local("./images/balkans_pollution_image_edited.jpg") 

# -----------------------------------------------------------------------------------------------------------------
st.title("Plan your trip: Forecasting seasonal pollutants")
components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """)
col1, col2, col3 = st.columns(3)
with col1:
        st.write("")
with col2:
        st.markdown("##### *- Ironhack Final Project -*")
        st.markdown("##### by **Marc Planas Marquès**")
with col3:
        st.write("")
# -----------------------------------------------------------------------------------------------------------------