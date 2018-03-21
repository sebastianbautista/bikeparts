import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def annual_avg_duration_by_region(df):
    regional_df = df.groupby('region_start_end')
    mean = regional_df['Minutes'].mean()
    median = regional_df['Minutes'].median()
    mean_annual_duration.append(mean)
    med_annual_duration.append(median)
    
for df in dfs:
    annual_avg_duration_by_region(df)
    
# set colnames and transpose for easier graphing
year = pd.Series(range(2010,2018))
mean_duration = pd.concat(mean_annual_duration, axis=1)
med_duration = pd.concat(med_annual_duration, axis=1)
mean_duration.columns = year
med_duration.columns = year
mean_duration = mean_duration.transpose().reset_index(level=0).add_prefix('Mean_').rename(columns={'Mean_index':'year'})
med_duration = med_duration.transpose().reset_index(level=0).add_prefix('Med_').rename(columns={'Med_index':'year'})

# regions for looping over
regions = list(df6.region_start_end.unique())
# remove a 'nan' from the list. For some reason .remove() wouldn't work
del regions[14]

# one plot per region
# ALX to FFX, MCN to ARL, FFX to MCS, ALX to MCN only have a single year of data
# which leads to the appearance of an empty plot
sns.set_style('darkgrid')
for region in regions:
    plt.plot('year', 'Mean_{}'.format(region), data=mean_duration, color='orange')
    plt.plot('year', 'Med_{}'.format(region), data=med_duration, color='blue')
    plt.title('Mean and median ride duration for {}'.format(region))
    plt.xlim(2010, 2017)
    plt.show()

'''
# plot all means - messy
sns.set_style('darkgrid')
for region in regions:
    plt.plot('year', 'Mean_{}'.format(region), data=mean_duration)
plt.show()
'''



    
