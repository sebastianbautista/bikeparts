import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import time; TIMESTR = time.strftime('%Y%m%d_%H%M%S')

''' Before using this, need to load the .spydata file containing
    dockless_df
'''

dockless_df['month'] = dockless_df['startdate'].dt.month
dockless_df['year'] = dockless_df['startdate'].dt.year
dockless_df['day'] = dockless_df['startdate'].dt.day
dockless_df['triplength'] = dockless_df['enddate'] - dockless_df['startdate']
f = lambda x: x.total_seconds()
dockless_df['triplengths'] = dockless_df['triplength'].map(f)

mobike_df = dockless_df.loc[dockless_df['operatorclean'] == 'mobike']
limebike_df = dockless_df.loc[dockless_df['operatorclean'] == 'lime']
ofo_df = dockless_df.loc[dockless_df['operatorclean'] == 'ofo']
spin_df = dockless_df.loc[dockless_df['operatorclean'] == 'spin']
jump_df = dockless_df.loc[dockless_df['operatorclean'] == 'jump']

sns.kdeplot(mobike_df['tripdistance']) # large, low level spike w/ outliers
plt.title('Mobike Trip Distance')
filename = '../img/' + 'mobike_distance_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(limebike_df['tripdistance']) # ibid
plt.title('Limebike Trip Distance')
filename = '../img/' + 'limebike_distance_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(ofo_df['tripdistance']) # outliers at 14k
plt.title('Ofo Trip Distance')
filename = '../img/' + 'ofo_distance_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(spin_df['tripdistance']) # looks pretty ok actually?
plt.title('Spin Trip Distance')
filename = '../img/' + 'spin_distance_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(jump_df['tripdistance']) # also looks ok
plt.title('Jump Trip Distance')
filename = '../img/' + 'jump_distance_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(mobike_df['triplengths']) # ok but with outliers
plt.title('Mobike Trip Duration')
filename = '../img/' + 'mobike_duration_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(limebike_df['triplengths']) # a lot of zeroes? few outliers
plt.title('Limebike Trip Duration')
filename = '../img/' + 'limebike_duration_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(ofo_df['triplengths']) # negatives
plt.title('Ofo Trip Duration')
filename = '../img/' + 'ofo_duration_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(spin_df['triplengths']) # looks ok
plt.title('Spin Trip Duration')
filename = '../img/' + 'spin_duration_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

sns.kdeplot(jump_df['triplengths']) # outliers
plt.title('Jump Trip Duration')
filename = '../img/' + 'jump_duration_' + TIMESTR + '.png'
#plt.savefig(fname=filename)
plt.show()

'''
corr = dockless_df.corr()
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
'''