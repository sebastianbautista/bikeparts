import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob2

#files = glob2.glob('C:/Users/slbau/CaBi//*.csv')

#for file in files:

# There's definitely a better way to do the below using glob and loops
df1 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2010-q4.csv')
df2 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2011-q1_2011-q2_2011-q3_2011-q4.csv')
df3 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2012-q1_2012-q2_2012-q3_2012-q4.csv')
df4 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2013-q1_2013-q2_2013-q3_2013-q4.csv')
df5 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2014-q1_2014-q2_2014-q3_2014-q4.csv')
df6 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2015-q1_2015-q2_2015-q3_2015-q4.csv')
df7 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2016-q1_2016-q2_2016-q3_2016-q4.csv')
df8 = pd.read_csv(r'C:\Users\slbau\CaBi\CABI_Daily_Trips_20180315_191537_2017-q1_2017-q2_2017-q3_2017-q4.csv')

df = df1.append([df2, df3, df4, df5, df6, df7, df8])

df[(df['region_start_end'] == 'WDC_to_WDC')]
