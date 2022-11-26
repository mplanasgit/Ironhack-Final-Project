from src.tools.sql_connection import engine
import pandas as pd

def get_country (country):
    query = f"""
    SELECT Datetime, Concentration, Year, Month, Day
    FROM `{country.lower()}`
    ;"""
    df = pd.read_sql_query(query, engine)
    return df