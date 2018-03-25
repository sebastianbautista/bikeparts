import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

''' Output not done. Meant to be total ride counts by member.
    Not 100% sure about the interpretation of the y-axis
    Looks like width is count of days and y-value is # of rides on a single day
    WIP - need to set up png names and output
'''

# Generate all counts by day

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

member_count = []
total_count = []

def daily_total(df):
    daily_df = df.groupby('start_date').size()
    total_count.append(daily_df)
    
def member_total(df):
    daily_df = df.groupby(['start_date', 'Member type']).size().unstack(level=-1).reset_index()
    member_count.append(daily_df)
    
for df in dfs:
    daily_total(df)
    member_total(df)
    
member_count = pd.concat(member_count)
total_count = pd.concat(total_count).reset_index().rename(columns={0: 'Total'})

final = member_count.merge(total_count, how='inner', on='start_date')

# datetime
final['date'] = pd.to_datetime(final['start_date'])
final['year'] = final['date'].dt.year 
final['month'] = final['date'].dt.month
final['weekday'] = final['date'].dt.weekday
final['weekday_name'] = final['date'].dt.weekday_name
final['quarter'] = final['date'].dt.quarter

TIMESTR = time.strftime('%Y%m%d_%H%M%S')

# plot
# total rides per month
sns.violinplot(x=final['month'], y=final['Total'])
plt.title('Total rides per month')
plt.show()

# total per weekday name
sns.violinplot(x=final['weekday_name'], y=final['Total'])
plt.title('Total rides per weekday name')
plt.show()

# casual per month
sns.violinplot(x=final['month'], y=final['Casual'])
plt.title('Casual rides per month')
plt.show()

# member per month
sns.violinplot(x=final['month'], y=final['Member'])
plt.title('Member rides per month')
plt.show()