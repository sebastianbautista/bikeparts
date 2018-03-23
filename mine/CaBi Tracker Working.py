import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

''' Station History Index
Generate index of first and last dock date, get total stations per day count 
and get list of retired stations that well need to account for with 
historical station information that we don't currently have.

Then leverage this index to plot historical # of stations  
and total station capacity (this will be inaccurate until 
we get historical station data)

'''

outage_df = pd.read_csv('~/CaBi/CaBi_Tracker_Outage_History_From_2011-05-01_To_2018-02-28.csv')

start_datetime = pd.to_datetime(outage_df['Start'])
end_datetime = pd.to_datetime(outage_df['End'])
# break dates down
outage_df['start_date'] = start_datetime.map(lambda x: x.date())
outage_df['end_date'] = end_datetime.map(lambda x: x.date())
outage_df['weekday'] = outage_df['start_date'].apply(lambda x: x.weekday())
outage_df['month'] = start_datetime.dt.month
outage_df['year'] = start_datetime.dt.year

# create full dummy, drop redundant empty dummy
outage_df = pd.concat([outage_df, pd.get_dummies(outage_df['Status'])], axis=1).drop('empty',axis=1)
outage_df.rename(columns={'full':'full_dummy'}, inplace=True)

# this is by month regardless of year. Month year fucked up and month throws errors in graph.
full_by_day = outage_df.groupby(['start_date','Status']).size().unstack(level=-1).reset_index()
full_by_month = outage_df.groupby(['month','Status']).size().unstack(level=-1).reset_index()
full_by_monthyear = outage_df.groupby(['year','month','Status']).size().unstack(level=[-2, -1]).reset_index()

# plot by day
# appears to be some kind of seasonal trend
sns.set_style('darkgrid')
plt.plot('start_date', 'empty', data=full_by_day)
plt.plot('start_date', 'full', data=full_by_day)
plt.title('# of full/empty docks by day')
plt.legend()
plt.show()

# plot by month
# seasonal trend more obvious
sns.set_style('darkgrid')
plt.plot('month', 'empty', data=full_by_month)
plt.plot('month', 'full', data=full_by_month)
plt.title('# of full/empty docks by discrete month')
plt.legend()
plt.show()

# pairplot illustrates common sense conclusion
# full and empty docks are positively correlated
# empty start docks = full destination docks
sns.pairplot(data=full_by_day)
