import matplotlib.pyplot as plt

plt.gcf().subplots_adjust(bottom=0.15)


def fix_date(input):
    import datetime
    try:
        input = datetime.datetime.strptime(input, '%m/%d/%Y %I:%M:%S %p')
    except:
        return np.NaN
    return input


def fix_hour(input):
    try:
        input = input.hour

    except:
        return np.NaN
    return input


def read_311_data(datafile):
    import pandas as pd

    # Read the file
    df = pd.read_csv(datafile)
    df = df[['Created Date', 'Closed Date', 'Agency', 'Borough']]

    # drop all rows that have any nans in them (note the easier syntax!)

    # df = df.dropna(how='any')

    # Convert times to datetime and create a processing time column

    df['Created Date'] = df['Created Date'].apply(fix_date)
    df['Closed Date'] = df['Closed Date'].apply(fix_date)

    # df['Created Date'] = df['Created Date'].apply(
    #    lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
    # df['Closed Date'] = df['Closed Date'].apply(
    #    lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
    df['processing_time'] = df['Closed Date'] - df['Created Date']
    df['start_time_window'] = df['Created Date'].apply(fix_hour)

    return df


import numpy as np

datafile = "311_data.csv"
data = read_311_data(datafile)
# %matplotlib inline
data['processing_hour'] = data['processing_time'].apply(lambda x: x / np.timedelta64(24, 'h'))
data[['processing_hour', 'start_time_window']].groupby('start_time_window').mean().plot(kind='bar', figsize=(8, 5.5)
                                                                                        )
plt.savefig("1.png", dpi=100)
plt.clf()
import seaborn as sns

data['processing_time'] = data['processing_time'].apply(lambda x: x / np.timedelta64(24, 'h'))
ax = sns.boxplot(y="processing_time", x="start_time_window", data=data)
fig = ax.get_figure()
fig.set_size_inches(8, 5.5)
fig.savefig("2.png", dpi=100)

df = data[['processing_time', 'Agency']].groupby('Agency').mean()
df = df.apply(lambda x: x.sort_values(ascending=False))
df.plot(kind='bar', figsize=(8, 5.5))
plt.savefig("3.png", dpi=100)
plt.clf()

df = data[['processing_time', 'Agency', 'Borough']].groupby(['Agency', 'Borough']).mean()
df = df.apply(lambda x: x.sort_values(ascending=False))
df = df.unstack('Borough')
COL_NUM = 2
ROW_NUM = 3
fig, axes = plt.subplots(ROW_NUM, COL_NUM, figsize=(12, 12))
for i, ((label, col)) in enumerate((df.iteritems())):
    ax = axes[int(i / COL_NUM), i % COL_NUM]
    col = col.sort_values(ascending=False)[:15]
    col.plot(kind='barh', ax=ax)
    ax.set_title(label[1])
plt.tight_layout
plt.savefig("4.png", dpi=100)
plt.clf()
