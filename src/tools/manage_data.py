import pandas as pd
import numpy as np
import src.tools.sql_query as sql
import src.tools.cleaning as clean
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ------------------------------------------------------------------------------------------------------------
# Function to categorize air quality based on concentration
def add_quality(row):
    if row['Avg historical conc. of PM10'] < 20:
        return 'Good'
    elif row['Avg historical conc. of PM10'] < 40:
        return 'Fair'
    elif row['Avg historical conc. of PM10'] < 50:
        return 'Moderate'
    elif row['Avg historical conc. of PM10'] < 100:
        return 'Poor'
    elif row['Avg historical conc. of PM10'] < 150:
        return 'Very Poor'
    elif row['Avg historical conc. of PM10'] > 150:
        return 'Extremely Poor'
    else:
        return "Concentration value couldn't be assessed!"

# ------------------------------------------------------------------------------------------------------------
def color_quality(index):
        if index == 'Good':
                return f'background-color: cyan'
        elif index == 'Fair':
                return f'background-color: lightgreen'
        elif index == 'Moderate':
                return f'background-color: yellow'
        elif index == 'Poor':
                return f'background-color: orange'
        elif index == 'Very Poor':
                return f'background-color: red'
        else:
                return f'background-color: purple'

# ------------------------------------------------------------------------------------------------------------
# Function to clean the return of query best months
def best_months(country, num_top):
    top = sql.get_best_months(country, num_top)
    month_dict = {1:'Jan',
            2:'Feb',
            3:'Mar',
            4:'Apr',
            5:'May',
            6:'Jun',
            7:'Jul',
            8:'Aug',
            9:'Sep',
            10:'Oct',
            11:'Nov',
            12:'Dec'}
    top = top.replace({"Month": month_dict})
    top['Air Quality Index'] = top.apply(lambda row: add_quality(row), axis = 1)
    top['Avg historical conc. of PM10'] = round(top['Avg historical conc. of PM10'],2)
    return top

# ------------------------------------------------------------------------------------------------------------
# Function to forecast
def build_forecast_SAMIRA(country):
    df = sql.get_country(country)
    df = clean.clean_forecast_easy(df)
    return df
