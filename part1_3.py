def fix_date(input):
    import datetime
    import numpy as np
    try:
        input = datetime.datetime.strptime(input, '%m/%d/%Y %I:%M:%S %p')
    except:
        return np.NaN
    return input


def fix_hour(input):

    import numpy as np

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

    import datetime
    df['Created Date'] = df['Created Date'].apply(fix_date)
    df['Closed Date'] = df['Closed Date'].apply(fix_date)

    # df['Created Date'] = df['Created Date'].apply(
    #    lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
    # df['Closed Date'] = df['Closed Date'].apply(
    #    lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
    df['processing_time'] = df['Closed Date'] - df['Created Date']
    df['start_time_window'] = df['Created Date'].apply(fix_hour)

    return df




datafile = "311_data.csv"
data = read_311_data(datafile)
data.to_csv('output1.csv', index=True)
