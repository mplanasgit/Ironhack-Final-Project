# Functions to clean dataframe

# Libraries
import datetime
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