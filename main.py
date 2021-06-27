import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

def pivot_low(df, order):
# Determining pivot low prices by iterating row by row to see if the price is the pivot price
    #col variable defines the name of the column for which pivot low is calculated
    col = ''
    if order == 1:
        col = 'Low'
    elif order > 1:
        col = f'{order-1}_Pivot_Low'
    tmpdf = pd.DataFrame(df.loc[:, col].dropna())
    tmpdf[f'{order}_Pivot_Low'] = np.NaN
    for x in range(1, len(tmpdf) - 1):
        if tmpdf.loc[tmpdf.index[x - 1], col] > tmpdf.loc[tmpdf.index[x], col] < tmpdf.loc[tmpdf.index[x + 1], col]:
            tmpdf.loc[tmpdf.index[x], f'{order}_Pivot_Low'] = tmpdf.loc[tmpdf.index[x], col]

    df[f'{order}_Pivot_Low'] = tmpdf[f'{order}_Pivot_Low']

def pivot_high(df, order):
# Determining pivot high prices by iterating row by row to see if the price is the pivot price
    #col variable defines the name of the column for which pivot high is calculated
    col = ''
    if order == 1:
        col = 'High'
    elif order > 1:
        col = f'{order-1}_Pivot_High'
    tmpdf = pd.DataFrame(df.loc[:, col].dropna())
    tmpdf[f'{order}_Pivot_High'] = np.NaN
    for x in range(1, len(tmpdf) - 1):
        if tmpdf.loc[tmpdf.index[x - 1], col] < tmpdf.loc[tmpdf.index[x], col] > tmpdf.loc[tmpdf.index[x + 1], col]:
            tmpdf.loc[tmpdf.index[x], f'{order}_Pivot_High'] = tmpdf.loc[tmpdf.index[x], col]

    df[f'{order}_Pivot_High'] = tmpdf[f'{order}_Pivot_High']


def better_pivots(df, order):
    tmpdf = df[[f'{order}_Pivot_Low', f'{order}_Pivot_High']].dropna(subset=[f'{order}_Pivot_High', f'{order}_Pivot_Low'], how='all')
    tmpdf[f'Clean_Pivot{order}'] = np.NaN
    value = None
    index = None

    column = f'{order}_Pivot_Low'
    list_to_drop = []

    for i in range(0,len(tmpdf)):
        if pd.notna(tmpdf.loc[tmpdf.index[i], f'{order}_Pivot_Low']) and pd.notna(tmpdf.loc[tmpdf.index[i], f'{order}_Pivot_High']):
            list_to_drop.append(tmpdf.index[i])

    tmpdf.drop(list_to_drop, inplace=True)

    for i in range(0, len(tmpdf)):
        if pd.notna(tmpdf.loc[tmpdf.index[i], column]):
            if value is not None:
                if value > tmpdf.loc[tmpdf.index[i], column]:
                    value = tmpdf.loc[tmpdf.index[i], column]
                    index = tmpdf.index[i]
            else:
                value = tmpdf.loc[tmpdf.index[i], column]
                index = tmpdf.index[i]
            if i == len(tmpdf)-1:
                tmpdf.at[index, f'Clean_Pivot{order}'] = value
        else:
            if (value is not None) or (i == len(tmpdf)):
                tmpdf.at[index, f'Clean_Pivot{order}'] = value
            value = None

    value = None

    column = f'{order}_Pivot_High'

    for i in range(0, len(tmpdf)):
        if pd.notna(tmpdf.loc[tmpdf.index[i], column]):
            if value is not None:
                if value < tmpdf.loc[tmpdf.index[i], column]:
                    value = tmpdf.loc[tmpdf.index[i], column]
                    index = tmpdf.index[i]
            else:
                value = tmpdf.loc[tmpdf.index[i], column]
                index = tmpdf.index[i]
            if i == len(tmpdf)-1:
                tmpdf.at[index, f'Clean_Pivot{order}'] = value
        else:
            if value is not None:
                tmpdf.at[index, f'Clean_Pivot{order}'] = value
            value = None

    df[f'Clean_Pivot{order}'] = tmpdf[f'Clean_Pivot{order}']
#    print(df[f'Clean_Pivot{order}'].to_string())








df = pdr.get_data_yahoo('TEAF', '20150101', '20210528')
df.drop('Adj Close', axis=1, inplace=True)
pivot_low(df, 1)

pivot_low(df, 2)

pivot_high(df,1)
pivot_high(df,2)

better_pivots(df, 1)
better_pivots(df, 2)

#plt.plot(df['Clean_Pivot1'].dropna(), 'r')
plt.plot(df['Clean_Pivot2'].dropna(), 'g')
#plt.plot(df['Close'])
plt.show()

