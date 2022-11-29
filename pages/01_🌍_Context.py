import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import pandas as pd
import src.tools.manage_data as manage

st.title('Air pollution link to disease')
st.subheader("*In 2019, 3.28 million global deaths were attributed to COPD, 40% of which were linked to air pollution.*")


image1=Image.open("./src/output/global/pm_europe.jpg")
image2=Image.open("./src/output/global/deaths_copd_europe.jpg")
st.image([image1,image2], width=500)


st.subheader('Air Quality Index')
air_df = pd.DataFrame({
    'Concentration of PM10 (µg/m3)': ['0 - 20', '20 - 40', '40 - 50', '50 - 100', '100 - 150', '150 - 1200'],
    'Air Quality Index': ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor', 'Extremely poor'],})
st.write('According to the [European Environment Agency](https://www.eea.europa.eu/), the index of **air quality** based on PM10 levels is the following:')
st.dataframe(air_df.style.applymap(manage.color_quality, subset=['Air Quality Index']))
st.write('Therefore, one should avoid long exposures to low quality air.')


f=codecs.open("./src/output/global/copd.html", 'r')
copd = f.read()

components.html(copd,height=600,scrolling=True)
