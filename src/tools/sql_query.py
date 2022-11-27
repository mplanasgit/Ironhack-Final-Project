from src.tools.sql_connection import engine
import pandas as pd

def get_country (country):
    query = f"""
    SELECT *
    FROM `{country.lower()}`
    ;"""
    df = pd.read_sql_query(query, engine)
    return df

def get_day(country, year, month, day):
    query = f"""
    SELECT *
    FROM `{country.lower()}`
    WHERE Year = {year}
    AND Month = {month}
    AND Day = {day}
    ;"""
    df = pd.read_sql_query(query, engine)
    return df

def get_best_months(country, num_limit):
    query = f"""
    SELECT Month, round(avg(Concentration),2) as 'Avg historical conc. of PM10' 
    FROM `{country.lower()}`
    GROUP BY Month
    ORDER BY round(avg(Concentration),2) ASC
    LIMIT {num_limit}
    ;"""
    df = pd.read_sql_query(query, engine)
    return df

def get_period(country, date_from, date_to):
    query = f"""
    SELECT Datetime, Concentration
    FROM `{country.lower()}`
    WHERE `Datetime` BETWEEN '{date_from}' AND '{date_to}'
    ;"""
    df = pd.read_sql_query(query, engine)
    return df


