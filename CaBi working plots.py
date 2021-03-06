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

# load in yearly data 
df0 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2010-q4.csv')
df1 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2011-q1_2011-q2_2011-q3_2011-q4.csv')
df2 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2012-q1_2012-q2_2012-q3_2012-q4.csv')
df3 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2013-q1_2013-q2_2013-q3_2013-q4.csv')
df4 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2014-q1_2014-q2_2014-q3_2014-q4.csv')
df5 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2015-q1_2015-q2_2015-q3_2015-q4.csv')
df6 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2016-q1_2016-q2_2016-q3_2016-q4.csv')
df7 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2017-q1_2017-q2_2017-q3_2017-q4.csv')

dfs = [df0, df1, df2, df3, df4, df5, df6, df7]

# annual mean and median, daily rides by member type
year = pd.Series(range(2010,2018))
casual_median = pd.Series()
member_median = pd.Series()
casual_mean = pd.Series()
member_mean = pd.Series()

def calc_annual_median_by_type(df):
    daily_rides_by_stack = df.groupby(['start_date', 'Member type']).size().unstack(level=[-1])
    casual_med = daily_rides_by_stack[['Casual']].median()
    member_med = daily_rides_by_stack[['Member']].median()
    casual_mean = daily_rides_by_stack[['Casual']].mean()
    member_mean = daily_rides_by_stack[['Member']].mean()
    return casual_med, member_med, casual_mean, member_mean

# there's definitely a better way to do this 
casual_med0, member_med0, casual_mean0, member_mean0 = calc_annual_median_by_type(df0)
casual_med1, member_med1, casual_mean1, member_mean1 = calc_annual_median_by_type(df1)
casual_med2, member_med2, casual_mean2, member_mean2 = calc_annual_median_by_type(df2)
casual_med3, member_med3, casual_mean3, member_mean3 = calc_annual_median_by_type(df3)
casual_med4, member_med4, casual_mean4, member_mean4 = calc_annual_median_by_type(df4)
casual_med5, member_med5, casual_mean5, member_mean5 = calc_annual_median_by_type(df5)
casual_med6, member_med6, casual_mean6, member_mean6 = calc_annual_median_by_type(df6)
casual_med7, member_med7, casual_mean7, member_mean7 = calc_annual_median_by_type(df7)

casual_median = pd.concat([casual_median, casual_med0, casual_med1, casual_med2, 
                           casual_med3, casual_med4, casual_med5, casual_med6, casual_med7], ignore_index=True)
member_median = pd.concat([member_median, member_med0, member_med1, member_med2, 
                           member_med3, member_med4, member_med5, member_med6, member_med7], ignore_index=True)
casual_mean = pd.concat([casual_mean, casual_mean0, casual_mean1, casual_mean2, 
                           casual_mean3, casual_mean4, casual_mean5, casual_mean6, casual_mean7], ignore_index=True)
member_mean = pd.concat([member_mean, member_mean0, member_mean1, member_mean2, 
                           member_mean3, member_mean4, member_mean5, member_mean6, member_mean7], ignore_index=True)

final = pd.DataFrame({'year': year, 'casual_median':casual_median, 
                      'member_median':member_median, 'casual_mean':casual_mean,
                      'member_mean':member_mean})

# plot
sns.set_style('darkgrid')
plt.plot('year', 'casual_median', data=final, linestyle='dashed', color='blue')
plt.plot('year', 'member_median', data=final, color='blue')
plt.plot('year', 'casual_mean', data=final, linestyle='dashed', color='orange')
plt.plot('year', 'member_mean', data=final,color='orange')
plt.title('Median/Mean Rides per Year by Member Type')
plt.legend()
plt.show()

# annual mean and median, ride duration for the entire system and by region

system_mean_duration = pd.Series()
system_med_duration = pd.Series()
regional_mean_duration = pd.DataFrame()
regional_med_duration = pd.DataFrame()

def duration_calc(df):
    system_mean = df['Minutes'].mean()
    system_med = df['Minutes'].median()
    regional_mean = df.groupby('region_start_end')['Minutes'].mean()
    regional_med = df.groupby('region_start_end')['Minutes'].median()
    return system_mean, system_med, regional_mean, regional_med

system_mean0, system_med0, regional_mean0, regional_med0 = duration_calc(df0)
system_mean1, system_med1, regional_mean1, regional_med1 = duration_calc(df1)
system_mean2, system_med2, regional_mean2, regional_med2 = duration_calc(df2)
system_mean3, system_med3, regional_mean3, regional_med3 = duration_calc(df3)
system_mean4, system_med4, regional_mean4, regional_med4 = duration_calc(df4)
system_mean5, system_med5, regional_mean5, regional_med5 = duration_calc(df5)
system_mean6, system_med6, regional_mean6, regional_med6 = duration_calc(df6)
system_mean7, system_med7, regional_mean7, regional_med7 = duration_calc(df7)

# need to figure out how to append all of these

'''
trips_by_member = df0.groupby(['start_date', 'region_start_end', 'Member type']).size().unstack(level=[-2, -1]) # getting count and then unstacking to keep by day
trips_by_member = pd.DataFrame(trips_by_member.to_records()).set_index('start_date') # cast to record then to df, then index to day
trips_by_member.columns = [hdr.replace("('", "").replace("', '", "_").replace("')", "") for hdr in trips_by_member.columns] # rename headers?
'''





