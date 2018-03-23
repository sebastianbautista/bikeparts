import psycopg2
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('~/git/Bikeshare-DC/') / '.env' 
load_dotenv(dotenv_path=env_path)

host = "capstone-bikeshare.cs9te7lm3pt2.us-east-1.rds.amazonaws.com"
port = 5432
database = "bikeshare"

user = os.environ.get("AWS_READONLY_USER")
password = os.environ.get("AWS_READONLY_PASS")

# Connect to aws postgres DB
conn = psycopg2.connect(host=host, user=user, port=port, password=password, database=database)
cur = conn.cursor()

# Query 
# dark_sky_raw = weather
# cabi_trips = trips
# as is, just pulls time, not datetime
# also capitalization doesn't seem to be an issue - returns all lower case
df = pd.read_sql("""SELECT
TO_TIMESTAMP(apparentTemperatureHighTime)::timestamp as apparentTemperatureHighTime
FROM dark_sky_raw;""", con=conn)
