import src.tools.model as mod
import streamlit as st

# Explanation
st.title('*PM10 Forecaster*')
st.write('')
st.subheader('Use our built-in SARIMA model')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.markdown('SARIMA(p,d,q)(P,D,Q)<sub>s</sub> = SARIMA(0,1,1)(0,1,2)<sub>12</sub>',unsafe_allow_html=True)
with col3:
    st.write(' ')

# Select a country to plot a line chart
dict_cities = {
    'Andorra':'Andorra la Vella','Albania':'Tirana','Austria':'Wien',
    'Belgium':'Bruxelles','Bosnia and Herzegovina':'Sarajevo','Bulgaria':'Sofia',
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
    st.write("The **RMSE** for the tested data is:", model_rmse)
with col3:
    st.write(' ')

st.write(' ')
st.write(' ')
st.subheader('Try your own parameters: SARIMA(p,d,q)(P,D,Q)s') 

# Model (with specified parameters)
col1, col2 = st.columns(2)
with col1:
    st.markdown('**Trend order**')
    p = st.number_input('Autoregression: Insert a value for **p**', min_value=0, max_value=4, value=0, step=1)
    d = st.number_input('Difference: Insert a value for **d**', min_value=0, max_value=4, value=1, step=1)
    q = st.number_input('Moving average: Insert a value for **q**', min_value=0, max_value=4, value=1, step=1)
with col2:
    st.markdown('**Seasonal order**')
    P = st.number_input('Autoregression: Insert a value for **P**', min_value=0, max_value=4, value=0, step=1)
    D = st.number_input('Difference: Insert a value for **D**', min_value=0, max_value=4, value=1, step=1)
    Q = st.number_input('Moving average: Insert a value for **Q**', min_value=0, max_value=4, value=2, step=1)
    s = st.number_input('Seasonal period: Insert a value for **s**', min_value=2, max_value=12, value=12, step=1)
# Model
fig, your_model_rmse = mod.model_SARIMA(country, p, d, q, P, D, Q, s)
st.plotly_chart(fig)
# RMSE
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.write("The **RMSE** of your model for the tested data is:", your_model_rmse)
    if your_model_rmse < model_rmse:
        st.write('Based on the RMSE, your model is better than ours!')
with col3:
    st.write(' ')