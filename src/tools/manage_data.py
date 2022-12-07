# Libraries
import src.tools.sql_query as sql
import src.tools.cleaning as clean

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
# Function to clean dataset before forecast
def build_forecast_SARIMA(country):
    df = sql.get_country(country)
    df = clean.clean_forecast_easy(df)
    return df

# ------------------------------------------------------------------------------------------------------------
# Function to add quality index in forecast
def add_quality_forecast(row):
    if row['Concentration'] < 20:
        return 'Good'
    elif row['Concentration'] < 40:
        return 'Fair'
    elif row['Concentration'] < 50:
        return 'Moderate'
    elif row['Concentration'] < 100:
        return 'Poor'
    elif row['Concentration'] < 150:
        return 'Very Poor'
    elif row['Concentration'] > 150:
        return 'Extremely Poor'
    else:
        return "Concentration value couldn't be assessed!"
    
# ------------------------------------------------------------------------------------------------------------
# Function to get best months in forecast
def best_months_forecast(df, num_ranking):
    # extract months
    df['Month'] = df.index.month
    df = df.sort_values(by=['Concentration'])
    # rename months
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
    df = df.replace({"Month": month_dict})
    # add air quality index
    df['Air Quality Index'] = df.apply(lambda row: add_quality_forecast(row), axis = 1)
    df['Concentration'] = round(df['Concentration'],2)
    df = df.reset_index()
    df = df[['Month','Concentration','Air Quality Index']]
    df = df.rename(columns={'Month':'Forecast Month','Concentration':'Forecast Concentration','Air Quality Index':'Forecast Air Quality Index'})
    return df[:num_ranking]