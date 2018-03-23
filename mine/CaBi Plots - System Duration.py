''' Output = systemwide average annual duration
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Daily Average/Median Duration System and Regions, annual median
# Daily Average/Median Duration System and Regions, annual mean

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

mean_annual_duration = []
med_annual_duration = []

# calculate mean and median duration from an input df
def average_duration(df):
    mean = df['Minutes'].mean()
    median = df['Minutes'].median()
    mean_annual_duration.append(mean)
    med_annual_duration.append(median)
    
# loop through all dfs
for df in dfs:
    average_duration(df)
   
# bring everything into one df
average_annual_duration = pd.DataFrame({'year': range(2010,2018), 'Mean_Duration_mins': mean_annual_duration,
                                        'Med_Duration_mins': med_annual_duration})
# plot
sns.set_style('darkgrid')
plt.plot('year', 'Mean_Duration_mins', data=average_annual_duration, color='orange')
plt.plot('year', 'Med_Duration_mins', data=average_annual_duration, color='blue')
plt.legend()
plt.title('System-wide mean and median annual ride duration, minutes')
TIMESTR = time.strftime("%Y%m%d_%H%M%S")
filename = '../img/' + 'Systemwide_Avg_Annual_Duration_' + TIMESTR + '.png'
plt.savefig(fname=filename)
plt.show()

''' Daily average duration below

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

# plot
sns.set_style('darkgrid')
plt.plot('start_date', 'Mean_Duration_mins', data=avg_duration, color='orange')
plt.plot('start_date', 'Med_Duration_mins', data=avg_duration, color='blue')
plt.show()

'''
