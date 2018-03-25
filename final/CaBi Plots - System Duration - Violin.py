import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('darkgrid')
import time

''' This script is meant to create violin plots for system-wide duration from 
    daily rolled up (mean, median) CaBi data.
    WIP - still working on using mean/med as a hue.
    Output = 4 pngs containing violin plots for systemwide mean/median duration
'''

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

# Daily average duration 
mean_duration = []
med_duration = []

def daily_average_duration(df):
    daily_df = df.groupby('start_date')
    mean = daily_df['Minutes'].mean()
    median = daily_df['Minutes'].median()
    mean_duration.append(mean)
    med_duration.append(median)
for df in dfs:
    daily_average_duration(df)

# creating and merging dataframes for plotting
mean_duration = pd.concat(mean_duration).reset_index(level=0).rename(columns={'Minutes': 'Mean_Duration_mins'})
med_duration = pd.concat(med_duration).reset_index(level=0).rename(columns={'Minutes': 'Med_Duration_mins'})
avg_duration = mean_duration.merge(med_duration, how='outer', left_on='start_date', right_on='start_date')
# pull out datetime stuff for graphing
avg_duration['date'] = pd.to_datetime(avg_duration['start_date'])


avg_duration['year'] = avg_duration['date'].dt.year 
avg_duration['month'] = avg_duration['date'].dt.month
avg_duration['weekday'] = avg_duration['date'].dt.weekday
avg_duration['weekday_name'] = avg_duration['date'].dt.weekday_name
avg_duration['quarter'] = avg_duration['date'].dt.quarter


TIMESTR = time.strftime('%Y%m%d_%H%M%S')

# could also try to turn mean/med into a column here (group by then unstack? or create column before merging?)
# then can use mean/med column as hue 

# plot means by year
sns.violinplot(x=avg_duration['year'], y=avg_duration['Mean_Duration_mins'])
plt.title('System-wide CaBi mean annual ride duration, minutes')
filename = '../img/' + 'Systemwide_Mean_Ride_Duration_by_Year_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()

# plot medians by year
sns.violinplot(x=avg_duration['year'], y=avg_duration['Med_Duration_mins'])
plt.title('System-wide CaBi median annual ride duration, minutes')
filename = '../img/' + 'Systemwide_Median_Ride_Duration_by_Year_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()

# plot means by discrete month
sns.violinplot(x=avg_duration['month'], y=avg_duration['Mean_Duration_mins'])
plt.title('System-wide CaBi mean ride duration by month, minutes')
filename = '../img/' + 'Systemwide_Mean_Ride_Duration_by_Month_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()

# plot means by weekday
sns.violinplot(x=avg_duration['weekday_name'], y=avg_duration['Mean_Duration_mins'])
plt.title('System-wide CaBi mean ride duration by weekday, minutes')
filename = '../img/' + 'Systemwide_Mean_Ride_Duration_by_Weekday_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()