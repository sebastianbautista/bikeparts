''' Input = all of the quarterly CaBi raw csvs.
	Loops through all of the quarterly csvs.
	Merges each of them with station and region data.
	Cleans date, time, day of week, etc. variables.
	Final loop creates yearly csvs.
	Output = (8) yearly csvs with cleaned datetime, station, and region data.
'''

## Compile Bikeshare Data ##

import pandas as pd
import time
import os
import sys
import re
from datetime import date
import calendar
import glob2


TIMESTR = time.strftime("%Y%m%d_%H%M%S") # timestamp for output filename

### Load Cabi Trip Data as Data Frame

Final_Daily_Rides = pd.DataFrame() # initialize df

all_header_files = glob2.glob('..//*.csv') # regex? for identifying all of the output files
FILE_LIST = []
FILE_LIST_all = []
counter = 0
for file in all_header_files: # iterate through the output csvs
    counter = counter +1 # increment counter - this becomes relevant when appending
    FILE = re.search('([2][0][0-9][0-9][-][a-z][0-4])',file) # regex for finding the csvs. returns a Match object
    FILE_LIST.append(FILE.group(0)) # appends the entire match/string; (1 or 2 would return first and second parenthesized subgroup, 1,2 would return tuple
    FILE_LIST_all.append(FILE.group(0)) # appends to the second list? also, FILE.group(0) is identical to FILE[0]
    trip_df = pd.read_csv(file) # read each csv into a df...
    trip_df['source'] = FILE # ... then create a new column containing the Match object(intentional? or did we want file name?)
    ### Derive Trip Date from Start Date time stamp
    start_datetime = pd.to_datetime(trip_df['Start date']) # string to datetime
    end_datetime = pd.to_datetime(trip_df['End date']) # string to datetime
    trip_df['start_date'] = start_datetime.map(lambda x: x.date()) # create columns for date in proper format
    trip_df['end_date'] = end_datetime.map(lambda x: x.date())
    ### 0-23, Military Time - EST
    trip_df['start_hour'] = start_datetime.dt.hour # create columns for hours
    trip_df['end_hour'] = end_datetime.dt.hour
    ### 0-6, 0 is Monday - 6 is Sunday
    trip_df['Weekday'] = trip_df['start_date'].apply(lambda x: x.weekday()) # create column for dow
    ### Append Region Code onto Trip Data
    station_info_df = pd.read_csv('../Output/CABI_Station_Info_20180307_080242.csv') # read in region data
    start_station_info_df = station_info_df.add_prefix('start_') # create new df with start_ 
    trip_df = trip_df.merge(start_station_info_df, left_on='Start station number',
                            right_on='start_short_name', how='left') # left join output csv with region data on start station num
    end_station_info_df = station_info_df.add_prefix('end_') # create new df with end_
    trip_df = trip_df.merge(end_station_info_df, left_on='End station number', # again, left join output csv with region data on start station num
                            right_on='end_short_name', how='left')
    trip_df['region_start_end'] = trip_df['start_region_code'] + \
        '_to_' + trip_df['end_region_code'] # create start/end region var by concatenating start and end region codes
    trip_df['station_start_end'] = trip_df['Start station'] + \
        '_to_' + trip_df['End station'] # same as above but for start/end station
    ### Milisecond per Minute 0.0000166667 
    trip_df['Minutes'] = 0.0000166667 * trip_df['Duration (ms)'] # converting duration into minutes
    '''There are a handful of trips that will be dropped
    because they are either warehouse trips or the station
    no longer exists,option to find location by name instead of
    station information'''
    # print(trip_df[(trip_df['region_start_end'].isnull()) & (
    # ~trip_df['station_start_end'].str.contains('6035 Warehouse'))]['station_start_end'].value_counts())
    
    ### Append to Final Dataframe
    Final_Daily_Rides = Final_Daily_Rides.append(trip_df) # append the trip_df we made above to the df initialized at the beginning
    if counter == 4: # every year, 
        final = '_'.join(str(v) for v in FILE_LIST) # cast the filenames to strings then join them with '_' between them 
        filename = "CABI_Daily_Trips_" + TIMESTR + "_" + str(final) + ".csv" # concat to form full filename string
        filepath = os.path.join("../Output", filename) # point to where to output the file
        Final_Daily_Rides.to_csv(filepath, index=False) # output file as csv, don't write row names
        FILE_LIST =[] # reinitialize file_list for the next year
        Final_Daily_Rides =pd.DataFrame() # reinitialize yearly df for next year
        counter = 0 # reset counter for the next year
    elif file == all_header_files[0]: # if it's the first file, just output this (depends on the first file being the oldest - look into glob order)
        final = '_'.join(str(v) for v in FILE_LIST)
        filename = "CABI_Daily_Trips_" + TIMESTR + "_" + str(final) + ".csv"
        filepath = os.path.join("../Output", filename)
        Final_Daily_Rides.to_csv(filepath, index=False)
        FILE_LIST =[]
        Final_Daily_Rides =pd.DataFrame()
        counter = 0
    elif len(FILE_LIST_all) == len(all_header_files): # if it's the last file, do the same as above but don't reset counter or file_list
        final = '_'.join(str(v) for v in FILE_LIST)
        filename = "CABI_Daily_Trips_" + TIMESTR + "_" + str(final) + ".csv"
        filepath = os.path.join("../Output", filename)
        Final_Daily_Rides.to_csv(filepath, index=False)
    # if none of the above are true, outer loop runs again and appends the next trip_df to final_daily_rides
    print(file)
    
    
#Weird Error for 2016-q3 File
#C:\Users\Noah\Anaconda3\lib\site-packages\IPython\core\interactiveshell.py:2698: DtypeWarning: Columns (3,5) have mixed types. Specify dtype option on import or set low_memory=False.
#interactivity=interactivity, compiler=compiler, result=result)
#C:/Users/Noah/cabi_data\2016-q3_trip_history_data.csv