''' Input = at least (1) of the yearly CaBi csvs
	Working file for exploring CaBi data and creating plots in seaborn.
	For now, testing with 2010q4 data
	Output = plots listed below
'''

# Daily Average/Median Member Type, annual median
# Daily Average/Median Member Type, annual mean
# Daily Average/Median Duration System and Regions, annual median
# Daily Average/Median Duration System and Regions, annual mean
# Daily Average/Median Duration DC to DC, Member Types
# Daily Average/Median Duration Member Type 2010-2017
# Daily Average/Median Duration System and Regions 2010-2017

# Generate station history index 
# 	Get total stations per day count
# 	Get list of retired stations that we'll need to account for with historical station info
# Generate bike history index (deprioritize until DDOT data)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df0 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2010-q4.csv')
df1 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2011-q1_2011-q2_2011-q3_2011-q4.csv')
df2 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2012-q1_2012-q2_2012-q3_2012-q4.csv')
df3 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2013-q1_2013-q2_2013-q3_2013-q4.csv')
df4 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2014-q1_2014-q2_2014-q3_2014-q4.csv')
df5 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2015-q1_2015-q2_2015-q3_2015-q4.csv')
df6 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2016-q1_2016-q2_2016-q3_2016-q4.csv')
df7 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_223118_2017-q1_2017-q2_2017-q3_2017-q4.csv')

dfs = [df0, df1, df2, df3, df4, df5, df6, df7]

# test

# daily median member type, annual median
final = pd.DataFrame()
final['year'] = range(2010,2018)
casual_median = pd.Series()
member_median = pd.Series()


for df in dfs:   
    daily_rides_by_member = df.groupby(['start_date', 'Member type']).size().unstack(level=[-1])
    casual_med = daily_rides_by_member[['Casual']].median()
    member_med = daily_rides_by_member[['Member']].median()
    casual_median.append(casual_med)
    member_median.append(member_med)
    
casual_mean = pd.Series()    
member_mean = pd.Series()



# ... annual mean

'''
trips_by_member = df0.groupby(['start_date', 'region_start_end', 'Member type']).size().unstack(level=[-2, -1]) # getting count and then unstacking to keep by day
trips_by_member = pd.DataFrame(trips_by_member.to_records()).set_index('start_date') # cast to record then to df, then index to day
trips_by_member.columns = [hdr.replace("('", "").replace("', '", "_").replace("')", "") for hdr in trips_by_member.columns] # rename headers?
'''





