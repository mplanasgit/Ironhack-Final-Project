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
    df = manage.build_forecast_SARIMA(country)
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
    # dict for the dataframes and their names
    dfs = {
        "Model" : model_data,
        "Actual data (- test)" : pd.DataFrame(train),
        "Test data" : pd.DataFrame(test)}

    # plot the data
    fig = go.Figure()
    fig.add_vrect(x0='2021-01-31', x1='2024-01-31', 
        line_width=0, fillcolor="blue", opacity=0.1, 
        annotation_text="Forecast", annotation_position="top left",
        annotation=dict(font_size=17))
    fig.update_layout(
        title=f"<b>PM10 Modelling for the city of {dict_cities[country]}</b>",
        xaxis_title="Year",
        yaxis_title="Concentration of PM10 (µg/m3)",
        font=dict(size=16))
    fig.update_layout(
        title={'y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'})

    for i in dfs:
        fig = fig.add_trace(go.Scatter(x = dfs[i].index,
                                    y = dfs[i].Concentration, 
                                    name = i))
        # if i == 'Actual data (- test)':
        #     fig.update_traces(line=dict(color='black',width=2))

    model_rmse = round(rmse(pred,test),2)
    return fig, model_rmse, model_data

# ------------------------------------------------------------------------------------------------------------
# Function that builds the model of SARIMA
def forecast_prophet(country):
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
    df = manage.build_forecast_SARIMA(country)
    test = df['Concentration'][-12:]
    df = df.reset_index()
    df = df.rename(columns={'date':'ds', 'Concentration':'y'})
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(df)
    future = model.make_future_dataframe(periods=37, freq='M')
    forecast = model.predict(future)
    pred = forecast[['ds','yhat']][-49:-37].set_index('ds')
    pred = pred['yhat']
    # build figure
    fig = plot_plotly(model, forecast)
    fig.update_layout(title=f"PM10 forecast for the city of {dict_cities[country]}",
                             xaxis_title="Year",
        yaxis_title="Concentration of PM10 (µg/m3)",
        font=dict(size=14))
    fig.update_layout(
        title={'y':0.94,'x':0.5,'xanchor':'center','yanchor':'top'})
    # errors
#     cutoffs = pd.date_range(start='2019-06-01', end='2020-07-01', freq='3M')
#     df_cv = cross_validation(model=model, horizon='90 days', cutoffs=cutoffs)

    return fig, pred, test