import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Daily Average/Median Member Type, annual median
# Daily Average/Median Member Type, annual mean

# load in yearly data 
df0 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2010-q4.csv')
df1 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2011-q1_2011-q2_2011-q3_2011-q4.csv')
df2 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2012-q1_2012-q2_2012-q3_2012-q4.csv')
df3 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2013-q1_2013-q2_2013-q3_2013-q4.csv')
df4 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2014-q1_2014-q2_2014-q3_2014-q4.csv')
df5 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2015-q1_2015-q2_2015-q3_2015-q4.csv')
df6 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2016-q1_2016-q2_2016-q3_2016-q4.csv')
df7 = pd.read_csv(r'~/CaBi/Output/CABI_Daily_Trips_20180315_191537_2017-q1_2017-q2_2017-q3_2017-q4.csv')

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