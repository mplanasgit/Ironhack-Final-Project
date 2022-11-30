# Libraries
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs

# Page configuration
st.set_page_config(
     page_title="PM10 Context",
     page_icon="🌍",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# -----------------------------------------------------------------------------------------------------------------

st.title('Air pollution and disease')
st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    st.subheader('Particulate Matter (PM)')
    st.markdown('- Not a single pollutant, but a mixture of many chemical species (solids and aerosols).')
    st.markdown('- Particles are defined by their diameter for air quality regulatory purposes.')
    st.markdown('- Those with a d < of 10 microns (PM10) are inhalable into the lungs and can induce adverse health effects, such as COPD.')
with col2:
    image=Image.open('./images/PM_size.png')
    st.image(image, use_column_width=False, width = 350)
# st.markdown('*from CALIFORNIA Air Resources Board, State of California*')

image0=Image.open('./images/COPD_facts.jpg')
st.image(image0)
st.markdown('*from Health Effects Institute. State of Global Air. 2020*')
st.subheader('')

# -----------------------------------------------------------------------------------------------------------------

st.markdown('#### In Europe, althoguh PM levels have slowly decreased over the years, COPD cases are steadily increasing')
st.markdown('')
image2=Image.open("./src/output/global/pm_europe.jpg")
image3=Image.open("./src/output/global/deaths_copd_europe.jpg")
st.image([image2,image3], width=500)
st.subheader('')
st.markdown('#### Evolution of deaths (% of population) in Europe')
f=codecs.open("./src/output/global/copd.html", 'r')
copd = f.read()
components.html(copd,height=600,scrolling=True)

# -----------------------------------------------------------------------------------------------------------------

st.title('')
st.markdown('#### Main objectives')
st.markdown('- To build an App to visualize PM10 historical data')
st.markdown('- To investigate the seasonality of PM10 in Europe')
st.markdown('- To forecast levels of PM10 in European cities')