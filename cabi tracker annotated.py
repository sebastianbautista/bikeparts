''' Input = CaBi tracker URL
	Defines a function used to pull daily data from CaBi tracker using requests.
	Loops through dates to pull outage data, converts to df, appends to list.
	Turns list to df, keep only 'empty' and 'full' statuses.
	Output as csv, zip, upload to GDrive.
	Output = zip in GDrive containing csv of daily outage data from CaBi tracker between d1 and d2
'''

import requests
import pandas as pd
import io
from datetime import date, timedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import zipfile

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

### above this is standard for PyDrive

def pull_daily_data(date):
    ''' pulls a date of outage data from Cabi Tracker'''
    params = {'s': date,
              'e': date} # start = end because this pulls a single day of data
    CaBiTrackerURl = "http://cabitracker.com/downloadoutage.php"
    urlData = requests.get(CaBiTrackerURl, params=params).content # accesses the response body, which is in utf-8, returns csv?
    rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8'))) # decode the data then read the resulting csv into a df
    return rawData


d1 = date(2011, 5, 1)  # start date
d2 = date(2018, 2, 28)  # end date
delta = d2 - d1         # timedelta


df_list = []
for i in range(delta.days + 1):
    date = (d1 + timedelta(days=i)) # increment the start date d1 by a day every loop
    date_df = pull_daily_data(date) # returns csv with a day of outage data, converts to df? doesn't pull_daily_data return a df?
    df_list.append(date_df) # appends df to list
    print("{} processed".format(date))

# Combine and Keep only "empty" and "full" statuses
combined_df = pd.concat(df_list, axis=0) # concatenate the daily dfs along the row axis
combined_df = combined_df[combined_df['Status'].isin(['empty', 'full'])].drop('Station Name') # keep the empty and full stations but drop station name

# Output dataframe as CSV
outname = "CaBi_Tracker_Outage_History_From_" + d1.strftime('%Y-%m-%d') + "_To_" + d2.strftime('%Y-%m-%d')
combined_df.to_csv(outname + ".csv", index=False) # write combined df to csv, don't write row names

### below this is standard for PyDrive

# Add CSV to zip
compression = zipfile.ZIP_DEFLATED
zf = zipfile.ZipFile(outname + ".zip", mode='w')
zf.write(outname + ".csv", compress_type=compression)
zf.close()

# Upload CSV to Google Drive
data_folder = '175Zhy6KRdgOwVhwqeZPANHCv6GvJJfvv'

file1 = drive.CreateFile({'title': outname,
                          "parents": [{"kind": "drive#fileLink", "id": data_folder}]})
file1.SetContentFile(outname + ".zip")  # Set content of the file from given string.
file1.Upload()