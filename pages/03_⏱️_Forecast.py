import src.tools.manage_data as manage
import streamlit as st
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from plotly.offline import iplot
import pandas as pd

dict_cities = {
    'Andorra':'Andorra la Vella','Albania':'Tirana','Austria':'Wien',
    'Bosnia and Herzegovina':'Sarajevo','Belgium':'Bruxelles','Bulgaria':'Sofia',
    'Switzerland':'Bern','Cypern':'Nicosia','Czech Republic':'Praha','Germany':'Berlin',
    'Denmark':'København','Estonia':'Tallinn','Spain':'Madrid','Finland':'Helsinki',
    'France':'Paris','United Kingdom':'London','Greece':'Athina','Croatia':'Zagreb',
    'Hungary':'Budapest','Ireland':'Dublin','Iceland':'Reykjavík','Italy':'Roma',
    'Lithuania':'Vilnius','Luxembourg':'Luxembourg','Latvia':'Riga','Montenegro':'Podgorica',
    'Malta':'Valletta','Netherlands':'Amsterdam','Norway':'Oslo','Poland':'Warszawa',
    'Portugal':'Lisboa','Romania':'Bucuresti','Serbia':'Belgrade','Sweden':'Stockholm',
    'Slovenia':'Ljubljana','Slovakia':'Bratislava','Kosovo':'Pristina'
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
    train, 
    order = my_order, 
    seasonal_order = my_seasonal_order, 
    freq='M'
).fit()

# Predict the test and forecast
model_data = pd.DataFrame(model.predict(start=1,end=len(train))).rename(columns={'predicted_mean':'Concentration'})
pred = model.predict(start=len(train), end=len(train) + 12)
forecast = model.predict(start=train.shape[0], end=train.shape[0] + 36)
forecast = pd.DataFrame(train.append(forecast)).rename(columns={0:'Concentration'})

# Plot
# fig = px.line(data_frame=model_data,)
# fig = plt.plot(forecast, color='r', label='Forecast')
# plt.axvspan(train.index[-1], forecast.index[-1], alpha=0.5, color='lightgrey')
# plt.plot(train, label='Actual data')
# plt.plot(test, label='Test data')
# plt.plot(model_data, label='Model')
# plt.legend()

# dict for the dataframes and their names
dfs = {"df1" : model_data, "df2": forecast, "df3" : pd.DataFrame(train), "df4" : pd.DataFrame(test)}

# plot the data
fig = go.Figure()

for i in dfs:
    fig = fig.add_trace(go.Scatter(x = dfs[i].index,
                                   y = dfs[i].Concentration, 
                                   name = i))


st.plotly_chart(fig)