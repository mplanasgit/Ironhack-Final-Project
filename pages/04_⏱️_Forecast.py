import src.tools.manage_data as manage
import streamlit as st
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go
import pandas as pd
from statsmodels.tools.eval_measures import rmse
import src.tools.sql_query as sql
from PIL import Image
import streamlit.components.v1 as components
import codecs

# Explanation
st.title('*PM10 Forecaster*')
st.write('')
st.write('')
st.write('XXX') 
st.markdown('- XXX')
st.markdown('- XXX')


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

# 1. Select a country to plot a line chart
country = st.selectbox("Choose one country", [country for country in dict_cities.keys()])

df = manage.build_forecast_SAMIRA(country)
# Split
train = df['Concentration'][:-13]
test = df['Concentration'][-13:]
# Model
my_order = (0,1,1)
my_seasonal_order = (0,1,2,12)
model = SARIMAX(
    df['Concentration'], 
    order = my_order, 
    seasonal_order = my_seasonal_order, 
    freq='M'
).fit()

# Predict the test and forecast
model_data = pd.DataFrame(model.predict(start=1,end=len(train) + 36)).rename(columns={'predicted_mean':'Concentration'})
pred = model.predict(start=len(train), end=len(train) + 12)
# forecast = model.predict(start=len(train), end=len(train) + 1)
# forecast = pd.DataFrame(train.append(forecast)).rename(columns={0:'Concentration'})

# dict for the dataframes and their names
dfs = {"Actual data (- test)" : pd.DataFrame(train), 
        "Model" : model_data, 
        "Test data" : pd.DataFrame(test)}

# plot the data
fig = go.Figure()
fig.add_vrect(x0='2021-01-31', x1='2023-01-31', 
    line_width=0, fillcolor="red", opacity=0.2, 
    annotation_text="Forecast", annotation_position="top left",
    annotation=dict(font_size=20))

fig.update_layout(
    title=f"PM10 Modelling for the city of {dict_cities[country]}",
    xaxis_title="Year",
    yaxis_title="Concentration of PM10 (µg/m3)")

for i in dfs:
    fig = fig.add_trace(go.Scatter(x = dfs[i].index,
                                   y = dfs[i].Concentration, 
                                   name = i))
    if i == 'Actual data (train)':
        fig.update_traces(
        line=dict(color='black',width=2))      

st.plotly_chart(fig)
st.write("The RMSE for the tested data is:", round(rmse(pred,test),2))