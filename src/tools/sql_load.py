# Functions to connect and load data into sql

# Libraries
import pandas as pd
import sqlalchemy as alch
from getpass import getpass


# -----------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------------------------------------
