import numpy as np
import pandas as pd
import os


cwd = os.getcwd()
dataFolder = cwd + '/dataFolder'
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)



def dataSort(df,date):
    df.sort_values(by=['vendorhardwareid','time'],inplace=True)
    del df['date']
    df.to_csv(dataFolder + '/' + date + '_sortedbusdata.csv',index=False)
    return 0

def dataSplit():
    df = pd.read_csv('dataset/metadata.csv')
    #df = pd.read_csv('multidate_roads.csv')
    print(df.shape)
    df[['date', 'time']] = df.logtime.str.split(expand=True)
    del df['logtime']
    df.sort_values(by=['date'], inplace=True)
    df.set_index(keys=['date'], drop=False, inplace=True)
    dates = df['date'].unique().tolist()

    for dateIndex in dates:
        dfsplit = df.loc[df.date == dateIndex]
        dataSort(dfsplit,dateIndex)
    return 0

dataSplit()


