import pandas as pd
import numpy as np

def rename_month(row):
    if row['Historical Conc. of PM10'] < 20:
        return 'Good'
    elif row['Historical Conc. of PM10'] < 40:
        return 'Fair'
    elif row['Historical Conc. of PM10'] < 50:
        return 'Moderate'
    elif row['Historical Conc. of PM10'] < 100:
        return 'Poor'
    elif row['Historical Conc. of PM10'] < 150:
        return 'Very Poor'
    elif row['Historical Conc. of PM10'] > 150:
        return 'Extremely Poor'
    else:
        return "Concentration value couldn't be assessed!"

def best_months(df, num_top):
    avg = df.groupby("Month")['Concentration'].mean().sort_values(ascending=True)
    month = avg.head(num_top).keys()
    concentration = np.round(avg.head(num_top).values,2)
    top = pd.DataFrame(month,concentration).reset_index().rename(columns={'index':'Historical Conc. of PM10'})
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
    top['Air Quality Index'] = top.apply(lambda row: rename_month(row), axis = 1)
    top = top[['Month','Historical Conc. of PM10', 'Air Quality Index']]
    return top