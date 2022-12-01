# Libraries
import src.tools.model as mod
import streamlit as st

# Page configuration
st.set_page_config(
     page_title="PM10 Forecast",
     page_icon="⏱️",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.markdown("""
<style>
.big {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------
# Explanation
st.title('*PM10 Forecaster*')
st.markdown('---')
st.subheader('Use our built-in SARIMA model')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.markdown('<p class="big"> SARIMA(p,d,q)(P,D,Q)<sub>s</sub> = SARIMA(0,1,1)(0,1,2)<sub>12</sub></p>',unsafe_allow_html=True)
with col3:
    st.write(' ')

# Select a country to plot a line chart
dict_cities = {
    'Bulgaria':'Sofia','Andorra':'Andorra la Vella','Albania':'Tirana','Austria':'Wien',
    'Belgium':'Bruxelles','Bosnia and Herzegovina':'Sarajevo',
    'Croatia':'Zagreb','Cypern':'Nicosia','Czech Republic':'Praha',
    'Denmark':'København','Estonia':'Tallinn','Finland':'Helsinki','France':'Paris',
    'Germany':'Berlin','Greece':'Athina','Hungary':'Budapest',
    'Iceland':'Reykjavík','Ireland':'Dublin','Italy':'Roma','Kosovo':'Pristina',
    'Latvia':'Riga','Lithuania':'Vilnius','Luxembourg':'Luxembourg',
    'Malta':'Valletta','Montenegro':'Podgorica','Netherlands':'Amsterdam','Norway':'Oslo',
    'Poland':'Warszawa','Portugal':'Lisboa','Romania':'Bucuresti','Serbia':'Belgrade',
    'Spain':'Madrid','Sweden':'Stockholm','Slovakia':'Bratislava','Slovenia':'Ljubljana',
    'Switzerland':'Bern','United Kingdom':'London' 
}
country = st.selectbox("Choose one country", [country for country in dict_cities.keys()])
# Model
fig, model_rmse = mod.model_SARIMA(country)
st.plotly_chart(fig)
# RMSE
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.write(f'<p class="big"> The RMSE for the tested data is: {model_rmse}</p>',unsafe_allow_html=True)
with col3:
    st.write(' ')

st.write(' ')
st.write(' ')
st.subheader('Try your own parameters: SARIMA(p,d,q)(P,D,Q)s') 

# Model (with specified parameters)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.title('')
    st.markdown('')
    st.markdown('📈 **Trend order (p,d,q):**')
    st.markdown('')
    st.title('')
    st.markdown('🍂 **Seasonal order (P,D,Q)s:**')
with col2:
    st.markdown('*Autoregression*')
    p = st.number_input('Insert a value of **p**', min_value=0, max_value=4, value=0, step=1)
    st.markdown('')
    P = st.number_input('Insert a value of **P**', min_value=0, max_value=4, value=0, step=1)
with col3:
    st.markdown('*Difference*')
    d = st.number_input('Insert a value of **d**', min_value=0, max_value=4, value=1, step=1)
    st.markdown('')
    D = st.number_input('Insert a value of **D**', min_value=0, max_value=4, value=1, step=1)
with col4:
    st.markdown('*Moving average*')
    q = st.number_input('Insert a value of **q**', min_value=0, max_value=4, value=1, step=1)
    st.markdown('')
    Q = st.number_input('Insert a value of **Q**', min_value=0, max_value=4, value=2, step=1)
with col5:
    st.markdown('*Seasonal period*')
    dummy = st.number_input('Trend does not have **s**', min_value=0, max_value=12, value=0, step=1, disabled = True)
    st.markdown('')
    s = st.number_input('Insert a value of **s**', min_value=2, max_value=12, value=12, step=1)
# Model
fig, your_model_rmse = mod.model_SARIMA(country, p, d, q, P, D, Q, s)
st.plotly_chart(fig)
# RMSE
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.write(f'<p class="big"> The RMSE of for the tested data is: {your_model_rmse}</p>',unsafe_allow_html=True)
    if your_model_rmse < model_rmse:
        st.write('<p class="big"> Based on the value of RMSE, you might have improved the model!</p>',unsafe_allow_html=True)
with col3:
    st.write(' ')