''' Graph isn't incredibly useful as-is; may want to switch to month-year instead of daily.
    Output = png containing daily mean/median ride duration by member type, DC to DC only.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Daily Average/Median Duration DC to DC, Member Types

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

mean_duration = []
med_duration = []
def daily_average_duration(df):
    # DC to DC only
    filtered_df = df[df.region_start_end == 'WDC_to_WDC']
    daily_df = filtered_df.groupby(['start_date', 'Member type']) 
    mean = daily_df['Minutes'].mean()
    median = daily_df['Minutes'].median()
    mean_duration.append(mean)
    med_duration.append(median)

for df in dfs:
    daily_average_duration(df)

# breaks down durations but yields 44 'unknown' obs. Ignoring for now.
mean_duration = pd.concat(mean_duration).unstack(level=-1).reset_index().rename(columns={'Casual': 'Mean_Casual','Member': 'Mean_Member'})
med_duration = pd.concat(med_duration).unstack(level=-1).reset_index().rename(columns={'Casual': 'Med_Casual','Member': 'Med_Member'})
avg_duration = mean_duration.merge(med_duration, on='start_date', how='inner').rename(columns={'index': 'start_date'})

# plot
# x axis being iffy with nbins
sns.set_style('darkgrid')
plt.plot('start_date', 'Mean_Casual', data=avg_duration, color='orange', linestyle='dashed')
plt.plot('start_date', 'Med_Casual', data=avg_duration, color='blue', linestyle='dashed')
plt.plot('start_date', 'Mean_Member', data=avg_duration, color='orange')
plt.plot('start_date', 'Med_Member', data=avg_duration, color='blue')
plt.legend()
plt.locator_params(axis='x', nbins=6)
plt.title('Daily mean and median ride duration by member type, DC to DC')
TIMESTR = time.strftime("%Y%m%d_%H%M%S")
filename = '../img/' + 'Avg_Daily_Duration_by_Member_DC_to_DC_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()

'''
# creating and merging dataframes for plotting
mean_duration = pd.concat(mean_duration).reset_index(level=0).rename(columns={'Minutes': 'Mean_Duration_mins'})
med_duration = pd.concat(med_duration).reset_index(level=0).rename(columns={'Minutes': 'Med_Duration_mins'})
avg_duration = mean_duration.merge(med_duration, how='outer', left_on='start_date', right_on='start_date')

# plot
sns.set_style('darkgrid')
plt.plot('start_date', 'Mean_Duration_mins', data=avg_duration, color='orange')
plt.plot('start_date', 'Med_Duration_mins', data=avg_duration, color='blue')
plt.show()
'''
