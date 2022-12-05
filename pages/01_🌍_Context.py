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
st.markdown("""
<style>
.big {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------

st.title('Air pollution and disease')
st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    st.subheader('Particulate Matter (PM)')
    st.markdown('- <p class="big"> Mixture of many chemical species (solids and aerosols).</p>', unsafe_allow_html=True)
    st.markdown('- <p class="big"> PM10 are inhalable into the lungs and can induce adverse health effects, such as COPD. </p>', unsafe_allow_html=True)
    image=Image.open('./images/copd.jpg')
    st.image(image, use_column_width=False, width=580)
    # st.markdown('*Health Effects Institute. State of Global Air. 2020*')
with col2:
    image=Image.open('./images/PM_size_comparison.jpg')
    st.image(image, use_column_width=False, width = 550)
# st.markdown('*from CALIFORNIA Air Resources Board, State of California*')
st.title('')

# -----------------------------------------------------------------------------------------------------------------

st.markdown('#### In Europe, althoguh PM levels have slowly decreased over the years, COPD cases are steadily increasing')
st.markdown('')
image2=Image.open("./src/output/global/pm_europe.jpg")
image3=Image.open("./src/output/global/deaths_copd_europe.jpg")
st.image([image2,image3], width=500)
# st.subheader('')
# st.markdown('#### Evolution of deaths (% of population) by COPD in Europe')
# f=codecs.open("./src/output/global/copd.html", 'r')
# copd = f.read()
# components.html(copd,height=600,scrolling=True)

# -----------------------------------------------------------------------------------------------------------------

st.title('')

st.markdown('## Main objectives and Applicability')
st.markdown('')
st.markdown('- ##### To build an App to visualize PM10 historical data: **PM10 Viewer** ')
st.markdown('- ##### To forecast levels of PM10 in European cities: **PM10 Forecaster**')
st.markdown('- ##### To investigate the seasonality of PM10 in Europe')