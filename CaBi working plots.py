''' Input = at least (1) of the yearly CaBi csvs
	Working file for exploring CaBi data and creating plots in seaborn.
	For now, testing with 2010q4 data
	Output = plots listed below
'''

# Daily Average/Median Member Type, annual median (1)
# Daily Average/Median Member Type, annual mean (1)
# Daily Average/Median Duration System and Regions, annual median (1)
# Daily Average/Median Duration System and Regions, annual mean (1)
# Daily Average/Median Duration DC to DC, Member Types (1)
# Daily Average/Median Duration Member Type 2010-2017 (1)
# Daily Average/Median Duration System and Regions 2010-2017 (1)

# Generate station history index 
# 	Get total stations per day count
# 	Get list of retired stations that we'll need to account for with historical station info
# Generate bike history index (deprioritize until DDOT data)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv('../Output/CABI_Daily_Trips_20180315_191537_2010-q4.csv')