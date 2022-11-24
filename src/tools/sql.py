# Functions to load data into sql

# Libraries
import pandas as pd
import sqlalchemy as alch
from getpass import getpass

# ------------------------------------------------------------------------------------------------------------
def table_to_sql_from_dict (db_name, dict_cities):
    '''This function connects to mysql and creates tables according to dictionary and directory path.
    '''
    # establish connection
    password = getpass("Please enter your password: ")
    connectionData = f"mysql+pymysql://root:{password}@localhost/{db_name}"
    engine = alch.create_engine(connectionData)
    print(engine)
    # create tables
    for country_code, country_city in dict_cities.items():
        df = pd.read_csv(f'../data/EEA/All/Date_extracted/{country_city[-1]}_pm10_extracted.csv')
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.to_sql(f"{country_city[0]}", index=False, con = engine) # if new city is added: if_exists="append"