import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

outage_df = pd.read_csv('~/CaBi/CaBi_Tracker_Outage_History_From_2011-05-01_To_2018-02-28.csv')

start_datetime = pd.to_datetime(outage_df['Start'])
end_datetime = pd.to_datetime(outage_df['End'])
# break dates down
outage_df['start_date'] = start_datetime.map(lambda x: x.date())
outage_df['end_date'] = end_datetime.map(lambda x: x.date())
outage_df['weekday'] = outage_df['start_date'].apply(lambda x: x.weekday())
outage_df['month'] = start_datetime.dt.month
# create full dummy, drop redundant empty dummy
outage_df = pd.concat([outage_df, pd.get_dummies(outage_df['Status'])], axis=1).drop('empty',axis=1)
outage_df.rename(columns={'full':'full_dummy'}, inplace=True)

# this is by month regardless of year. Need month-year
full_by_day = outage_df.groupby(['start_date','Status']).size().unstack(level=-1).reset_index()
full_by_month = outage_df.groupby(['month','Status']).size().unstack(level=-1).reset_index()

# plot by day
sns.set_style('darkgrid')
plt.plot('start_date', 'empty', data=full_by_day)
plt.plot('start_date', 'full', data=full_by_day)
plt.legend()
plt.show()

# plot by month
sns.set_style('darkgrid')
plt.plot('month', 'empty', data=full_by_day)
plt.plot('month', 'full', data=full_by_day)
plt.legend()
plt.show()
