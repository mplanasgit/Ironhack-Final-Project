# Libraries
import streamlit as st
from PIL import Image
import src.tools.sql_query as sql
import src.tools.manage_data as manage
import plotly.express as px 
import datetime as datetime
import src.tools.visualization_streamlit as viss

# Page configuration
st.set_page_config(
     page_title="PM10 Historical data",
     page_icon="🌐",
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
# Explanation
st.title('*PM10 Viewer*')
st.markdown('---')
st.subheader('Historical data for European cities')

# -----------------------------------------------------------------------------------------------------------------
# Plotting timeseries for each capital present in the dict
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

# Select a country to plot a line chart
# Adjust text position
col1, col2 = st.columns(2)
with col1:
        country = st.selectbox("Choose one country, I will return the historical records of its capital", [country for country in dict_cities.keys()])
with col2:
        st.write(' ')
# Query
data = sql.get_country(country)
# Title
st.write('')
st.write(f"##### Here's the evolution of PM10 for the capital of **{country}**: ", f'**{dict_cities[country]}**')
# Custom legend
legend = Image.open("./src/output/time_series/legend_timeseries_jpg.jpg")
# Adjust text position
col1, col2, col3 = st.columns(3)
with col1:
        st.markdown(' ')
        st.markdown('Seasons have been colored according to the following:')
with col2:
        st.write(' ')
        st.image(legend, width=350)
with col3:
        st.markdown('')
# Define figure
fig = viss.plot_timeseries(data)
# Show plot
st.plotly_chart(fig)

# -----------------------------------------------------------------------------------------------------------------
# When is the best time of the year to visit the country?
st.subheader(f'When is the best time to visit {dict_cities[country]}?')
# Adjust text position
col1, col2 = st.columns(2)
with col1:
        num_top = st.slider('Select the total number of months to show in the ranking:', 1, 12, 1)
with col2:
        st.write(' ')
top = manage.best_months(country, num_top)
if num_top == 1:
        st.write(f'This is the best month to visit {dict_cities[country]}:')
        st.dataframe(top.style.applymap(manage.color_quality, subset=['Air Quality Index']))
else:
        st.write(f'These are the {num_top} best months to visit {dict_cities[country]}:')
        st.dataframe(top.style.applymap(manage.color_quality, subset=['Air Quality Index']))

# -----------------------------------------------------------------------------------------------------------------
# How was the pollution on a given period of time?
st.title('')
st.subheader(f'Inspect the levels of PM10 in {dict_cities[country]} in a given day or specific period of time')
st.markdown("Please select the desired date(s). To see the PM10 levels during a single day, select the same date in the *From* and *To* date widgets.")

col1, col2, col3, col4 = st.columns(4)
with col1:
        st.write('')
with col2:
        date_from = st.date_input("**From**",
        datetime.date(2018, 9, 3), 
        min_value = datetime.date(2013,1,1), 
        max_value = datetime.date(2021,1,1))
with col3:
        date_to = st.date_input("**To**",
        datetime.date(2018, 9, 3), 
        min_value = datetime.date(2013,1,1), 
        max_value = datetime.date(2021,1,1))
with col4:
        st.write('')
st.write("")

if date_from == date_to:
        st.write(f'These were the levels of PM10 on day {date_from} in the city of {dict_cities[country]}:')
        # extract    
        year, month, day = int(date_from.year), int(date_from.month), int(date_from.day)
        # query
        data_date = sql.get_day(country,year,month,day)
        data_date = data_date[~data_date.Datetime.duplicated()]
        # plot
        if data_date.shape[0] == 0:
                st.write(f"There are no records for the city of {dict_cities[country]} on day {date_from} in our database")
        elif data_date.shape[0] == 1:
                st.write(f"There is only one record of PM10 for the city of {dict_cities[country]} on day {date_from}:", data_date[['Datetime','Concentration']])
        else:
                fig_date = viss.plot_timeseries_period(data_date)
                st.plotly_chart(fig_date)

else:
        st.write(f'These were the levels of PM10 from {date_from} to {date_to} in the city of {dict_cities[country]}:')
        # query
        data_period = sql.get_period(country,date_from,date_to)
        data_period = data_period[~data_period.Datetime.duplicated()]
        if data_period.shape[0] == 0:
                st.write(f"There are no records for the city of {dict_cities[country]} from {date_from} to {date_to} in our database.")
        elif data_period.shape[0] == 1:
                st.write(f"There is only one record of PM10 for the city of {dict_cities[country]} in the specified dates:", data_period[['Datetime','Concentration']])
        else:
                fig_period = viss.plot_timeseries_period(data_period)
                st.plotly_chart(fig_period)
