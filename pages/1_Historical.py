import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs
import pandas as pd
import src.tools.sql_query as sql
import plotly.express as px 


# 1. Create a bar chart
st.write("""# Plotting page""")






# -----------------------------------------------------------------------------------------------------------------
# Plotting timeseries

dict_cities = {
    'Andorra':'Andorra_la_Vella','Albania':'Tirana','Austria':'Wien',
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
# 2. Clean the dataframe for plotting
data_for_plot = sql.get_country(country)
# 3. Title
st.write(f"""Here's the evolution of PM10 for the capital of {country}: """, f'**{dict_cities[country]}**')
# 4. Define figure
fig = px.line(data_frame=data_for_plot, x='Datetime', y="Concentration")

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
        annotation_text=f'<b>{value}</b>', 
        annotation_position="top right",
        annotation=dict(font_size=12, font_color='grey'),
        opacity=0.5)
# Add seasons
for i in range(2013,2021):
        fig.add_vrect(x0=f'{i}-03-20', x1=f'{i}-06-20', fillcolor='green', opacity=0.2, line_width=0)
        fig.add_vrect(x0=f'{i}-06-21', x1=f'{i}-09-22', fillcolor='orange', opacity=0.2, line_width=0)
        fig.add_vrect(x0=f'{i}-09-23', x1=f'{i}-12-20', fillcolor='brown', opacity=0.2, line_width=0)
        fig.add_vrect(x0=f'{i}-12-21', x1=f'{i}-12-31', fillcolor='blue', opacity=0.2, line_width=0)
        fig.add_vrect(x0=f'{i}-01-01', x1=f'{i}-03-19', fillcolor='blue', opacity=0.2, line_width=0)
fig.update_traces(line_color='black', line_width=1)
# 5. Show plot
st.plotly_chart(fig)