import pandas as pd
import numpy as np
import src.tools.sql_query as sql

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
    top = top[['Month','Avg historical conc. of PM10', 'Air Quality Index']]
    return top