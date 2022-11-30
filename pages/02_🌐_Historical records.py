import streamlit as st
from PIL import Image
import src.tools.sql_query as sql
import src.tools.manage_data as manage
import plotly.express as px 
import datetime as datetime
import src.tools.visualization_streamlit as viss

# -----------------------------------------------------------------------------------------------------------------

# Explanation
st.title('*PM10 Viewer*')
st.markdown('An App to **easily** visualize historical data of the **PM10** pollutant for a city of interest')
st.write('')
st.subheader('Historical data for European cities')
st.markdown('- Select a country from the dropdown menu')
st.markdown('- The App will return the historical records of the capital of that country')
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------
# Plotting timeseries
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
country = st.selectbox("Choose one country", [country for country in dict_cities.keys()])
# Query
data = sql.get_country(country)
# Title
st.write('')
st.write(f"##### Here's the evolution of PM10 for the capital of **{country}**: ", f'**{dict_cities[country]}**')
# Custom legend
st.write(f"""Seasons have been colored according to the following legend:""")
legend = Image.open("./src/output/time_series/legend_timeseries_jpg.jpg")
st.image(legend, use_column_width=False, width=350)
# Define figure
fig = viss.plot_timeseries(data)
# Show plot
st.plotly_chart(fig)

# -----------------------------------------------------------------------------------------------------------------

# When is the best time of the year to visit the country?
st.subheader(f'When is the best time to visit {dict_cities[country]}?')

num_top = st.slider('Select the total number of months to show in the ranking:', 0, 12, 1)
top = manage.best_months(country, num_top)
if num_top == 1:
        st.write(f'This is the best month to visit {dict_cities[country]}:')
        st.dataframe(top.style.applymap(manage.color_quality, subset=['Air Quality Index']))
else:
        st.write(f'These are the {num_top} best months to visit {dict_cities[country]}:')
        st.dataframe(top.style.applymap(manage.color_quality, subset=['Air Quality Index']))

# -----------------------------------------------------------------------------------------------------------------
st.write('')
st.write('')
# How was the pollution on a given period of time?
st.subheader(f'Inspect the levels of PM10 in {dict_cities[country]} in a given day or specific period of time')
st.write("Please select the desired date(s). To see the PM10 levels during a single day, select the same date in the *From* and *To* date widgets.")

date_from = st.date_input(
    "From",
    datetime.date(2018, 9, 3), 
    min_value = datetime.date(2013,1,1), 
    max_value = datetime.date(2021,1,1))
date_to = st.date_input(
    "To",
    datetime.date(2018, 9, 3), 
    min_value = datetime.date(2013,1,1), 
    max_value = datetime.date(2021,1,1))

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
                fig_date = px.line(data_frame=data_date, x='Datetime', y="Concentration")
                fig_date.update_traces(line_color='black', line_width=1)
                fig_date.update_xaxes( 
                title_text = "Hours of day",
                title_font = {"size": 15},
                title_standoff = 10)
                fig_date.update_yaxes( 
                        title_text = "Concentration [µg/m3]",
                        title_font = {"size": 15},
                        title_standoff = 10)
                air_quality = {0: 'Good', 20:'Fair', 40:'Moderate', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
                for key, value in air_quality.items():
                        fig_date.add_hline(
                        y=key, 
                        line_dash="dot",
                        line_color='black',
                        annotation_text=f'<b>{value}</b>', 
                        annotation_position="top right",
                        annotation=dict(font_size=12, font_color='black'),
                        opacity=0.5)
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
                fig_period = px.line(data_frame=data_period, x='Datetime', y="Concentration")
                fig_period.update_traces(line_color='black', line_width=1)
                fig_period.update_xaxes( 
                title_text = "Period of time",
                title_font = {"size": 15},
                title_standoff = 10)
                fig_period.update_yaxes( 
                        title_text = "Concentration [µg/m3]",
                        title_font = {"size": 15},
                        title_standoff = 10)
                air_quality = {0: 'Good', 20:'Fair', 40:'Moderate', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
                for key, value in air_quality.items():
                        fig_period.add_hline(
                        y=key, 
                        line_dash="dot",
                        line_color='black',
                        annotation_text=f'<b>{value}</b>', 
                        annotation_position="top right",
                        annotation=dict(font_size=12, font_color='black'),
                        opacity=0.5)
                st.plotly_chart(fig_period)
