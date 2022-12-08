import src.tools.manage_data as manage
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tools.eval_measures import rmse
from prophet import Prophet
from prophet.plot import plot_plotly

# ------------------------------------------------------------------------------------------------------------
# Function that builds the model of SARIMA
def model_SARIMA(country, p=0, d=1, q=1, P=0, D=1, Q=2, s=12):
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
    'Switzerland':'Bern','United Kingdom':'London' }
    df = manage.build_forecast(country)
    # Split
    train = df['Concentration'][:-12]
    test = df['Concentration'][-12:]
    # Model
    my_order = (p,d,q)
    my_seasonal_order = (P,D,Q,s)
    model = SARIMAX(
        df['Concentration'], 
        order = my_order, 
        seasonal_order = my_seasonal_order, 
        freq='M'
    ).fit()
    # Predict the test and forecast
    model_data = pd.DataFrame(model.predict(start=1,end=len(train) + 48)).rename(columns={'predicted_mean':'Concentration'})
    pred = model.predict(start=len(train)+1, end=len(train) + 12)

    # plot the data
    fig = go.Figure()
    fig.add_vrect(x0='2021-01-31', x1='2024-01-31', 
        line_width=0, fillcolor="blue", opacity=0.05, 
        annotation_text="<b>Forecast &#8594;</b>", annotation_position="top left",
        annotation=dict(font_size=18))
    fig.add_vline(x='2021-01-31', line_width=1, line_dash="dot", line_color="blue")
    fig.update_layout(
        title=f"<b> SARIMA({p},{d},{q})({P},{D},{Q})<sub>{s}</sub> PM10 forecast for the city of {dict_cities[country]}</b>",
        xaxis_title="Year",
        yaxis_title="Concentration of PM10 (µg/m3)",
        font=dict(size=16))
    fig.update_layout(
        title={'y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'})

    # add data to plot
    fig.add_trace(go.Scatter(x = model_data.index,
                                y = model_data.Concentration, 
                                name = "Model",
                                mode = "lines"))
    fig.add_trace(go.Scatter(x = pd.DataFrame(train).index,
                                y = pd.DataFrame(train).Concentration, 
                                name = "Actual data (- test)",
                                mode = "lines+markers",
                                marker=dict(size=4,color='black',line=dict(color='black', width=0.5))))
    fig.add_trace(go.Scatter(x = pd.DataFrame(test).index,
                                y = pd.DataFrame(test).Concentration, 
                                name = "Test data",
                                mode = "lines+markers",
                                marker=dict(color='green',line=dict(color='green', width=0.1))))                   
    model_rmse = round(rmse(pred,test),2)
    return fig, model_rmse, model_data

# ------------------------------------------------------------------------------------------------------------
# Function that builds the model of Facebook Prophet
def model_prophet(country):
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
    'Switzerland':'Bern','United Kingdom':'London' }
    df = manage.build_forecast(country)
    # train = df['Concentration'][:-12]
    test = df['Concentration'][-12:]
    df = df.reset_index()
    df = df.rename(columns={'date':'ds', 'Concentration':'y'})
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(df)
    future = model.make_future_dataframe(periods=37, freq='M')
    forecast = model.predict(future)
    model_data = forecast[['ds','yhat']].set_index('ds').rename(columns={'yhat':'Concentration'})
    pred = model_data[-49:-37]['Concentration']
    # build figure
    fig = plot_plotly(model, forecast)
    fig.update_layout(title=f"<b>PM10 forecast for the city of {dict_cities[country]}</b>",
                             xaxis_title="Year",
        yaxis_title="Concentration of PM10 (µg/m3)",
        font=dict(size=16))
    fig.update_layout(
        title={'y':0.94,'x':0.5,'xanchor':'center','yanchor':'top'})
    fig.add_vrect(x0='2021-01-31', 
                x1='2024-01-31', 
                line_width=0, fillcolor="blue", opacity=0.05, 
                annotation_text="<b>Forecast &#8594;</b>", annotation_position="top left",
                annotation=dict(font_size=18))
    fig.add_vline(x='2021-01-31', line_width=1, line_dash="dot", line_color="blue")
    fig.add_trace(go.Scatter(x = pd.DataFrame(test).index,
                                y = pd.DataFrame(test).Concentration, name = "Test",
                                marker=dict(color='green',line=dict(color='green', width=0.5))))
    
    model_rmse = round(rmse(pred,test),2)

    return fig, model_rmse, model_data