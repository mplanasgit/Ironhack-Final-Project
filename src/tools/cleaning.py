# Functions to clean dataframe

# Libraries
import pandas as pd

# ------------------------------------------------------------------------------------------------------------
def keep_columns (df, list_cols):
    '''This function keeps the important columns of a dataframe.
    Args
    :df: df. the dataframe
    :list_columns: list. includes the names of the columns to be kept
    Return
    :df: df. the dataframe without columns
    '''
    df = df[[c for c in list_cols]]
    return df

# ------------------------------------------------------------------------------------------------------------
def transform_datetime (df, col_name):
    '''This function transforms the values of a column into datetime format.
    Args
    :df: df. the dataframe
    :col_name: str. the name of the column where dates should be transformed
    '''
    df[col_name] = pd.to_datetime(df[col_name])
    # df = df.drop_duplicates(subset = col_name)
    df = df.set_index(col_name).sort_values(by=col_name, ascending = True)
    df.index = df.index.rename('Datetime')
    return df

# ------------------------------------------------------------------------------------------------------------
def average_concentration_city (df, col_name, country_code, city, pollutant):
    '''This function takes a df and gets the average concentration of a pollutant.
    Args
    :df: df. the dataframe
    :list_cols: list of str. the list of columns to keep
    :col_name: the column name where dates should be transformed to datetime
    :country_code: str. the code of the country
    :city: str. the name of the city
    :pollutant: str. the pollutant
    '''
    df1 = transform_datetime(df, col_name)
    df1['Concentration'] = df1['Concentration'].interpolate()
    df_city = pd.DataFrame(df1.groupby(level='Datetime')['Concentration'].mean())
    df_city['Concentration'] = df_city['Concentration'].round(2)
    df_city['Country_code'] = country_code
    df_city['City'] = city
    df_city['Pollutant'] = pollutant
    return df_city

# ------------------------------------------------------------------------------------------------------------
def average_concentration_city_country (df, col_name, country_code, country_city, pollutant):
    '''This function takes a df and gets the average concentration of a pollutant.
    Args
    :df: df. the dataframe
    :list_cols: list of str. the list of columns to keep
    :col_name: the column name where dates should be transformed to datetime
    :country_code: str. the code of the country
    :country_city: lst. first element is the name of the country, second element the name of the city
    :pollutant: str. the pollutant
    '''
    df1 = transform_datetime(df, col_name)
    df1['Concentration'] = df1.groupby([df1.index.month], sort=False)['Concentration'].apply(lambda x: x.fillna(x.mean())) #changed this, before it was = df1['Concentration'].interpolate()
    df_city = pd.DataFrame(df1.groupby(level='Datetime')['Concentration'].mean())
    df_city['Concentration'] = df_city['Concentration'].round(2)
    df_city['Country_code'] = country_code
    df_city['Country'] = country_city[0]
    df_city['City'] = country_city[-1]
    df_city['Pollutant'] = pollutant
    return df_city

# ------------------------------------------------------------------------------------------------------------

dict_cities = {
    'AD':['Andorra','Andorra_la_Vella'],'AL':['Albania','Tirana'],'AT':['Austria','Wien'],
    'BA':['Bosnia and Herzegovina','Sarajevo'],'BE':['Belgium','Bruxelles'],'BG':['Bulgaria','Sofia'],
    'CH':['Switzerland','Bern'],'CY':['Cypern','Nicosia'],'CZ':['Czech Republic', 'Praha'], 'DE':['Germany','Berlin'],
    'DK':['Denmark','København'],'EE':['Estonia','Tallinn'],'ES':['Spain','Madrid'],'FI':['Finland','Helsinki'],
    'FR':['France','Paris'],'GB':['United Kingdom','London'],'GR':['Greece','Athina'],'HR':['Croatia','Zagreb'],
    'HU':['Hungary','Budapest'],'IE':['Ireland','Dublin'],'IS':['Island','Reykjavík'],'IT':['Italy','Roma'],
    'LT':['Lithuania','Vilnius'],'LU':['Luxembourg','Luxembourg'],'LV':['Latvia','Riga'],'ME':['Montenegro','Podgorica'],
    'MT':['Malta','Valletta'],'NL':['Netherlands','Amsterdam'],'NO':['Norway','Oslo'],'PL':['Poland','Warszawa'],
    'PT':['Portugal','Lisboa'],'RO':['Romania','Bucuresti'],'RS':['Serbia','Belgrade'],'SE':['Sweden','Stockholm'],
    'SI':['Slovenia','Ljubljana'],'SK':['Slovakia','Bratislava'],'XK':['Kosovo','Pristina']
}

def save_avg_concentration_city (dict_cities, col_name = 'DatetimeEnd', pollutant = 'PM10'):
    '''This function averages the pollutant concentration for each country/city in the dictionary
    and saves the csv file in the corresponding folder.
    Args
    :dict_cities: dict. key = country_code ('XX' format), value = lst of ['country_name','city']
    '''
    for country_code, country_city in dict_cities.items():
        try:
            df = pd.read_csv(f'../data/EEA/{country_city[-1]}/{country_city[-1]}_combined_pm10.csv')
            df1 = average_concentration_city_country(df, col_name, country_code, country_city, pollutant)
            df1.to_csv(f'../data/EEA/All/{country_city[-1]}_pm10.csv')
            print(f'file created for {country_city[-1]}')
        except:
            print(f'Error encountered for {country_city[-1]}')

# ------------------------------------------------------------------------------------------------------------
def extract_date(dict_cities):
    for country_code, country_city in dict_cities.items():
        try:
            df = pd.read_csv(f'../data/EEA/All/{country_city[-1]}_pm10.csv')
            df = df.drop_duplicates(subset = "Datetime")
            df['Year'] = pd.DatetimeIndex(df['Datetime']).year
            df['Month'] = pd.DatetimeIndex(df['Datetime']).month
            df['Day'] = pd.DatetimeIndex(df['Datetime']).day
            df.to_csv(f'../data/EEA/All/Date_extracted/{country_city[-1]}_pm10_extracted.csv', index = False)
            print(f'file created for {country_city[-1]}')
        except:
            print(f'Error encountered for {country_city[-1]}')

# ------------------------------------------------------------------------------------------------------------
# Function to clean data for forecast
def clean_forecast_yearly(df, freq):
    df = df[~df.Datetime.duplicated()]
    df = df.set_index('Datetime')
    # redefine index
    idx = pd.period_range(min(df.index),max(df.index),freq=freq).to_timestamp()
    df = df.reindex(idx)
    # add year,month,day
    df['Year'] = pd.DatetimeIndex(df.index).year
    df['Month'] = pd.DatetimeIndex(df.index).month
    df['Day'] = pd.DatetimeIndex(df.index).day
    # fill nan with mean of that month
    df['Concentration'] = df.groupby(['Year', 'Month'], sort=False)['Concentration'].apply(lambda x: x.fillna(x.mean()))
    # group by month and year
    df = df.groupby(by=[df.index.month, df.index.year]).agg('mean').reset_index()
    # extract and rebuild date with only year and month
    df['date'] = df['level_0'].astype(str) + '-' + df['level_1'].astype(str)
    df.index = pd.to_datetime(df['date'])
    # reorder by index
    df = df.resample('M').last()
    df = df[['Concentration']]
    return df

def clean_forecast_easy(df):
    # group by month and year
    df = df[:-1]
    df = df.groupby(by=['Month', 'Year']).agg('mean').reset_index()
    # rebuild date with only year and month
    df['date'] = df['Year'].astype(str) + '-' + df['Month'].astype(str)
    df.index = pd.to_datetime(df['date'])
    # reorder by index
    df = df.resample('M').last()
    df = df[['Concentration']]
    return df