import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
# -----------------------------------------------------------------------------------------------------------------

st.title('Air pollution and disease')
st.write('')

st.subheader('Particulate Matter')
st.markdown('- Airborne **particulate matter (PM)** is not a single pollutant, but rather is a mixture of many chemical species. It is a complex mixture of solids and aerosols.')
st.markdown('- Particles are defined by their diameter for air quality regulatory purposes. Those with a diameter of 10 microns or less (PM10) are inhalable into the lungs and can induce adverse health effects, such as COPD.')
image0=Image.open('./images/COPD_facts.jpg')
st.image(image0)
st.markdown('*from Health Effects Institute. State of Global Air. 2020*')
st.write('')
st.write('')

# image1=Image.open('./images/PM_size.png')
# st.image(image1, width=400)
# st.markdown('*from CALIFORNIA Air Resources Board, State of California*')

st.markdown('#### In Europe, althoguh PM levels have slowly decreased over the years, COPD cases are steadily increasing')
st.write('')
image2=Image.open("./src/output/global/pm_europe.jpg")
image3=Image.open("./src/output/global/deaths_copd_europe.jpg")
st.image([image2,image3], width=500)
st.write('')
st.write('')
st.markdown('#### Evolution of deaths (% of population) in Europe')
f=codecs.open("./src/output/global/copd.html", 'r')
copd = f.read()
components.html(copd,height=600,scrolling=True)
