import os
import time
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import psycopg2


''' This script pulls all Dark Sky raw data from AWS.
    In progress. 4/4/2018
'''

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

host = "capstone-bikeshare.cs9te7lm3pt2.us-east-1.rds.amazonaws.com"
port = 5432
database = "bikeshare"

user = os.environ.get("AWS_READONLY_USER")
password = os.environ.get("AWS_READONLY_PASS")

# Connect to aws postgres DB
conn = psycopg2.connect(host=host, user=user, port=port, password=password, database=database)
cur = conn.cursor()

# Finish this query!
query = """
SELECT apparenttemperaturehigh, apparenttemperaturehightime,
        apparenttemperaturelow, apparenttemperaturelowtime,
        cloudcover, dewpoint, humidity, moonphase,
        precipaccumulation, precipintensity, precipintensitymax,
        precipintensitymaxtime, precipprobability, preciptype,
        pressure,
        (date_part('hour', to_timestamp(sunsettime)) +
        date_part('minute', to_timestamp(sunsettime))/60) as timeofday
        FROM dark_sky_raw LIMIT 1 """

darksky_df = pd.read_sql(query, con=conn)