''' Input = (2) links to .json data
	Grabs the CaBi station and region data in json format, cleans it up, merges them together.
	Takes two json files as inputs, outputs csv with station and region joined on region name and region id.
	Output = (1) station data csv. 
	This is merged with the CaBi data later.
'''

####CaBi_Stations


import pandas as pd
import requests
import numpy as np
import time
import os

### Load station information
station_url = "https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json"
stations = requests.get(station_url).json() # decode json data and store in variable
station_df = pd.DataFrame(stations['data']['stations']) # read the data row of the stations column of the json data into a df?
station_df = station_df[['lat', 'lon', 'region_id', 'short_name']].copy() # ? of the stations data, grab these four (not sure about copy) ?

### Default any missing region ids to DC (only example as of 2/21 is new station at Anacostia Park)
station_df['region_id'] = np.where(
    station_df['region_id'].isnull(), 42, station_df['region_id']) # if region id is missing, set it to 42 (DC), else keep the same

### Convert region_id to str from float
station_df['region_id'] = station_df['region_id'].astype(int).astype(str) # cast to int in order to cast to str

### Load region information
region_url = "https://gbfs.capitalbikeshare.com/gbfs/en/system_regions.json"
regions = requests.get(region_url).json()
regions_df = pd.DataFrame(regions['data']['regions']) # decode json data, store in variable, then read into dataframe

### Merge region information onto stations
station_df = station_df.merge(
    regions_df, left_on='region_id', right_on='region_id', how='left') # left joining stationdf on regionsdf on region id
station_df.rename(index=str, columns={'name': 'region_name'}, inplace=True) # ? rename 'name' column from regionsdf as 'region_name' but unsure about index=str ?
print(len(station_df))
print(station_df['region_name'].value_counts()) # prints number of unique region names

### Define Abbreviations for each region
# dictionary mapping locations to abbreviations
region_code = {'Washington, DC': 'WDC',
               'Arlington, VA': 'ARL',
               'Montgomery County, MD (South)': 'MCS',
               'Montgomery County, MD (North)': 'MCN',
               'Alexandria, VA': 'ALX',
               'Fairfax, VA': 'FFX'}

region_code_series = pd.Series(region_code, name='region_code') # creates vector (Series) just containing region code values (abbr)
region_code_series.index.name = 'region_name' # inserts region names as index for series
region_code_df = region_code_series.reset_index() # creates a df with a numeric index and region names as a new column
station_df = station_df.merge(
    region_code_df, left_on='region_name', right_on='region_name', how='left') # left joins stationdf and regioncodedf on region name to form new stationdf
station_df.drop(['region_name', 'region_id'], inplace=True, axis=1) # drop region name and region id (are they redundant? check)

### Output DataFrame as CSV with timestamp
TIMESTR = time.strftime("%Y%m%d_%H%M%S") # current time for timestamp purposes
filename = "CABI_Station_Info_" + TIMESTR + ".csv" # generates filename with timestamp
filepath = os.path.join("../Output", filename) # concatenates filepath and name for full local filepath
station_df.to_csv(filepath, index=False) # finally, exports df as a csv, don't write row names (index)