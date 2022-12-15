# Libraries
import streamlit as st
import src.tools.sql_query as sql
import src.tools.visualization_streamlit as viss
import streamlit.components.v1 as components
import codecs
from PIL import Image

# Page configuration
st.set_page_config(
     page_title="PM10 Seasonality",
     page_icon="🍂",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# -----------------------------------------------------------------------------------------------------------------
# Explanation
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.title('PM10 Seasonality')
with col3:
    st.write(' ')

st.markdown('---')
image=Image.open('./images/variability_index_calculation.jpg')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(' ')
with col2:
    st.image(image, width=350)
with col3:
    st.markdown('')

# Plot: Seasonality index by city
seasonality = sql.get_country('seasonality_index')
fig = viss.plot_seasonality_index(seasonality)
st.plotly_chart(fig)

# -----------------------------------------------------------------------------------------------------------------
st.markdown('#### The cities with the highest variability index are geographically related')

# Map: Seasonality index by city
f=codecs.open("./src/output/global/seasonality_index_map.html", 'r')
seasonality_map = f.read()
components.html(seasonality_map,height=600,scrolling=False)

# Map of Balkans
st.markdown('')
image0=Image.open('./images/Balkan_Peninsula.png')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(' ')
with col2:
    st.markdown('')
    st.image(image0)
with col3:
    st.write(' ')

# News article
st.write(' ')
image1 = Image.open('./images/balkans_pollution_news.jpg')
st.image(image1)