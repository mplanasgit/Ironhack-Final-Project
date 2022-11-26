import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import pandas as pd
import src.tools.sql_query as sql
import src.tools.manage_data as manage
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import datetime as datetime

# Explanation
st.title('*PM10 Viewer*')
st.write('An App to easily visualize PM10 historical data')
st.write('')
st.write('')
st.subheader('Historical data for European cities')
st.write('Here you can **easily** visualize historical data of the **PM10** pollutant for a city of interest') 
st.markdown('- Select a country from the dropdown menu')
st.markdown('- The App will return the historical data of the capital of that country')
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
    'Bosnia and Herzegovina':'Sarajevo','Belgium':'Bruxelles','Bulgaria':'Sofia',
    'Switzerland':'Bern','Cypern':'Nicosia','Czech Republic':'Praha','Germany':'Berlin',
    'Denmark':'København','Estonia':'Tallinn','Spain':'Madrid','Finland':'Helsinki',
    'France':'Paris','United Kingdom':'London','Greece':'Athina','Croatia':'Zagreb',
    'Hungary':'Budapest','Ireland':'Dublin','Island':'Reykjavík','Italy':'Roma',
    'Lithuania':'Vilnius','Luxembourg':'Luxembourg','Latvia':'Riga','Montenegro':'Podgorica',
    'Malta':'Valletta','Netherlands':'Amsterdam','Norway':'Oslo','Poland':'Warszawa',
    'Portugal':'Lisboa','Romania':'Bucuresti','Serbia':'Belgrade','Sweden':'Stockholm',
    'Slovenia':'Ljubljana','Slovakia':'Bratislava','Kosovo':'Pristina'
}

# 1. Select a country to plot a line chart
country = st.selectbox("Choose one country", [country for country in dict_cities.keys()])
# 2. Query
data = sql.get_country(country)
# 3. Title
st.write('')
st.write(f"##### Here's the evolution of PM10 for the capital of **{country}**: ", f'**{dict_cities[country]}**')
# Custom legend
st.write(f"""Seasons have been colored according to the following legend:""")
legend = Image.open("./src/output/time_series/legend_timeseries_jpg.jpg")
st.image(legend, use_column_width=False, width=350)
# 4. Define figure
fig = px.line(data_frame=data, x='Datetime', y="Concentration")
fig.update_traces(line_color='black', line_width=1)
# Modify axes labels
fig.update_xaxes( 
        title_text = "Year",
        title_font = {"size": 15},
        title_standoff = 10)
fig.update_yaxes( 
        title_text = "Concentration [µg/m3]",
        title_font = {"size": 15},
        title_standoff = 10)
# Add air quality thresholds
air_quality = {0: 'Good', 20:'Moderate', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
for key, value in air_quality.items():
    fig.add_hline(
        y=key, 
        line_dash="dot",
        line_color='black',
        annotation_text=f'<b>{value}</b>', 
        annotation_position="top right",
        annotation=dict(font_size=12, font_color='black'),
        opacity=0.5)
# Add seasons
for i in range(2013,2022):
        fig.add_vrect(x0=f'{i}-03-20', x1=f'{i}-06-20', fillcolor='green', opacity=0.15, line_width=1)
        fig.add_vrect(x0=f'{i}-06-21', x1=f'{i}-09-22', fillcolor='orange', opacity=0.15, line_width=1)
        fig.add_vrect(x0=f'{i}-09-23', x1=f'{i}-12-20', fillcolor='brown', opacity=0.15, line_width=1)
        fig.add_vrect(x0=f'{i}-12-21', x1=f'{i}-12-31', fillcolor='blue', opacity=0.15, line_width=1)
        fig.add_vrect(x0=f'{i}-01-01', x1=f'{i}-03-19', fillcolor='blue', opacity=0.15, line_width=1)
# 5. Show plot
st.plotly_chart(fig)

# -----------------------------------------------------------------------------------------------------------------

# When is the best time of the year to visit the country?
st.subheader(f'When is the best time to visit {dict_cities[country]}?')

num_top = st.slider('Select the total number of months to show in the ranking:', 0, 12, 1)
top = manage.best_months(country, num_top)
if num_top == 1:
        st.write(f'This is the best month to visit {dict_cities[country]}:', top)
else:
        st.write(f'These are the {num_top} best months to visit {dict_cities[country]}:', top)

# -----------------------------------------------------------------------------------------------------------------

st.write('')
# How was the pollution on that specific day?
st.subheader(f'Want to inspect the levels of PM10 of {dict_cities[country]} in a given day?')

date = st.date_input(
    "Select the desired date",
    datetime.date(2016, 7, 6), 
    min_value = datetime.date(2013,1,1), 
    max_value = datetime.date(2021,1,2))

st.write(f'These were the levels of PM10 on day {date} in {dict_cities[country]}:')

# extract    
year, month, day = int(date.year), int(date.month), int(date.day)
# query
data_date = sql.get_day(country,year,month,day)
# plot
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
air_quality = {0: 'Good', 20:'Moderate', 50:'Poor', 100:'Very Poor', 150:'Extremelly Poor'}
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