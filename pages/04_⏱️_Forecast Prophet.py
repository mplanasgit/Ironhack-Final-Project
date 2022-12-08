# Libraries
import src.tools.model as mod
import streamlit as st
import src.tools.manage_data as manage
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

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
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.title('*PM10 Forecaster*')
with col3:
    st.write(' ')
st.markdown('---')

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

# Model, prophet, SARIMA
fig_prophet, prophet_rmse, prophet_data = mod.model_prophet(country)
fig_sarima, sarima_rmse, sarima_data = mod.model_SARIMA(country)

# Plot fig
st.plotly_chart(fig_prophet)

# RMSE
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.write(f'<p class="big"> The RMSE of <b>Prophet</b> for the tested data is: <b>{prophet_rmse}</b></p>',unsafe_allow_html=True)
    st.write(f'<p class="big"> The RMSE with <b>SARIMA</b> would have been: <b>{sarima_rmse}</b></p>',unsafe_allow_html=True)
with col3:
    st.write(' ')

# -----------------------------------------------------------------------------------------------------------------
# When is the best time of the year to visit the country?
st.write(' ')
st.write(' ')
st.markdown('---')
st.subheader(f'When is the best time to visit {dict_cities[country]} in 2023?')
# Adjust text position
col1, col2 = st.columns(2)
with col1:
        num_top = st.slider('Select the total number of months to show in the ranking:', 1, 12, 1)
with col2:
        st.write(' ')
# get best historical months
top_historical = manage.best_months(country, num_top)
# get modelled data for 2023
forecast_2023 = prophet_data[-13:]
forecast_2023 = forecast_2023[:12]
# get best months of the modelled data
top_forecast = manage.best_months_forecast(forecast_2023,num_top)

# show different things depending on num on ranking
if num_top == 1:
        st.write(f'This is the best month to visit {dict_cities[country]} in 2023:')
else:
        st.write(f'These are the {num_top} best months to visit {dict_cities[country]} in 2023:')

col1, col2 = st.columns(2)
with col1:
        st.markdown('#### Historical')
        st.dataframe(top_historical.style.applymap(manage.color_quality, subset=['Air Quality Index']))
with col2:
        st.markdown('#### Forecast')
        st.dataframe(top_forecast.style.applymap(manage.color_quality, subset=['Air Quality Index']))