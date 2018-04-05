import os
import time
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import psycopg2


''' This script pulls and cleans all Dark Sky raw data from AWS.
    In progress - need to create weather_time dummies using 'summary' column.
    Output = csv containing cleaned weather data (optional)
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

# Query Dark Sky Raw
test = pd.read_sql("""SELECT (date_part('hour', to_timestamp(sunsettime)) +
                              date_part('minute', to_timestamp(sunsettime))/60) as time
                   FROM dark_sky_raw LIMIT 100;""", con=conn)

'''
Could try something like
SELECT CONVERT(char, sunrisetime, 114) as sunrisetime
114 - 24 hour clock
120 - 24 hr clock with date
'''