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

# Finish this query! Need to add rain dummies!
query = """
SELECT apparenttemperaturehigh,
        (date_part('hour', to_timestamp(apparenttemperaturehightime)) +
        date_part('minute', to_timestamp(apparenttemperaturehightime))/60) as apparenttemperaturehightime,
        apparenttemperaturelow,
        (date_part('hour', to_timestamp(apparenttemperaturelowtime)) +
        date_part('minute', to_timestamp(apparenttemperaturelowtime))/60) as apparenttemperaturelowtime,
        cloudcover, dewpoint, humidity, moonphase,
        precipaccumulation, precipintensity, precipintensitymax,
        (date_part('hour', to_timestamp(precipintensitymaxtime)) +
        date_part('minute', to_timestamp(precipintensitymaxtime))/60) as precipintensitymaxtime,
        precipprobability, preciptype,
        pressure,
        CASE WHEN preciptype = 'rain' THEN 1 ELSE 0 END as rain_dummy,
        CASE WHEN preciptype = 'snow' THEN 1 ELSE 0 END as snow_dummy,
        (date_part('hour', to_timestamp(sunrisetime)) +
        date_part('minute', to_timestamp(sunrisetime))/60) as sunrisetime,
        (date_part('hour', to_timestamp(sunsettime)) +
        date_part('minute', to_timestamp(sunsettime))/60) as sunsettime,
        temperaturehigh,
        (date_part('hour', to_timestamp(temperaturehightime)) +
        date_part('minute', to_timestamp(temperaturehightime))/60) as temperaturehightime,
        temperaturelow,
        (date_part('hour', to_timestamp(temperaturelowtime)) +
        date_part('minute', to_timestamp(temperaturelowtime))/60) as temperaturelowtime,
        (date_part('hour', to_timestamp(day_time)) +
        date_part('minute', to_timestamp(day_time))/60) as day_time,
        visibility, weather_date, windbearing, windspeed,
        to_date(cast(weather_date as TEXT), 'YYYY-MM-DD') as date,
        date_part('year', to_date(cast(weather_date as TEXT), 'YYYY-MM-DD')) as year,
        date_part('quarter', to_date(cast(weather_date as TEXT), 'YYYY-MM-DD')) as quarter,
        date_part('month', to_date(cast(weather_date as TEXT), 'YYYY-MM-DD')) as month,
        date_part('dow', to_date(cast(weather_date as TEXT), 'YYYY-MM-DD')) as day_of_week
        FROM dark_sky_raw"""

darksky_df = pd.read_sql(query, con=conn)