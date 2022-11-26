import pandas as pd
import streamlit as st
import os
import src.tools.sql_query as sql

def load_dataframe ():
    df = pd.read_pickle("data/clean.pkl")
    return df