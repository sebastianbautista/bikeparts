from pathlib import Path
from dotenv import load_dotenv
import os
import time; TIMESTR = time.strftime('%Y%m%d_%H%M%S')
import psycopg2
import pandas as pd

''' This script pulls all dockless raw data from AWS.
    In progress. 4/5/2018
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
SELECT * FROM dockless_trips"""

dockless_df = pd.read_sql(query, con=conn)
