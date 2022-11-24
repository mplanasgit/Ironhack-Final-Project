# Functions to clean dataframe

# Libraries
import datetime
import pandas as pd
import os

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
    df1['Concentration'] = df1['Concentration'].interpolate()
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
            df['Year'] = pd.DatetimeIndex(df['Datetime']).year
            df['Month'] = pd.DatetimeIndex(df['Datetime']).month
            df['Day'] = pd.DatetimeIndex(df['Datetime']).day
            df.to_csv(f'../data/EEA/All/Date_extracted/{country_city[-1]}_pm10_extracted.csv', index = False)
            print(f'file created for {country_city[-1]}')
        except:
            print(f'Error encountered for {country_city[-1]}')
