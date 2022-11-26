import sqlalchemy as alch
from getpass import getpass
import os
from dotenv import load_dotenv


load_dotenv()

db_name = "europe_pm10"
password=os.getenv("sql_password")
connectionData = f"mysql+pymysql://root:{password}@localhost/{db_name}"
engine = alch.create_engine(connectionData)