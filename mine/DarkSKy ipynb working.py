import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import seaborn as sns; sns.set_style('darkgrid')

df = pd.read_csv(r'~\git\Bikeshare-DC\data\Dark_Sky_2010_2017.csv', parse_dates=[0], infer_datetime_format=True)

# creating weather dummies
df = pd.concat([df, pd.get_dummies(df['precipType'])], axis=1)
df.rename(columns = {'rain': 'rain_dummy','snow': 'snow_dummy'}, inplace = True)

# converting Unix time to human-readable time
timevars = ['apparentTemperatureHighTime','apparentTemperatureLowTime','precipIntensityMaxTime',
           'sunriseTime','sunsetTime','temperatureHighTime','temperatureLowTime', 'time']
for var in timevars:
    df[var] = pd.to_datetime(df[var],unit='s')

df['year'] = df['date'].dt.year 
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.weekday
df['weekday_name'] = df['date'].dt.weekday_name
df['quarter'] = df['date'].dt.quarter

# KDE with Scikit-Learn
def kde_sklearn(x, x_grid, bandwidth=0.2):
    kde_skl = KernelDensity(bandwidth=bandwidth)
    kde_skl.fit(x[:, np.newaxis])
    # score_samples returns log-likelihood of samples
    pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    return np.exp(pdf)

def density(column, bandwidth=0.2):
    sns.set_style('darkgrid')
    x_grid = np.linspace(df.loc[:, column].min(), df.loc[:, column].max())
    x = df.loc[:, column]
    pdf = kde_sklearn(x, x_grid, bandwidth=bandwidth)
    ax.plot(x_grid, pdf, color='blue', alpha=0.5, lw=1)
    ax.set_title('KDE for {}'.format(column))
    plt.show()
    
fig, ax = plt.subplots()
density('daylightHours', bandwidth=1)