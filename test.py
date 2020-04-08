import pandas as pd, numpy as np, matplotlib.pyplot as plt, os, sys

# Data 
datapath = './../COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
datafiles = [datapath + x for x in os.listdir(datapath) if x.endswith('global.csv')]
datafiles_us = [datapath + x for x in os.listdir(datapath) if x.endswith('US.csv')]

# Params
topn = 5
if len(sys.argv) > 1:
    topn = int(sys.argv[1])

plotfrom = '2020-03-01'

def readdf(filename):
    raw = pd.read_csv(filename)
    df = raw.drop(columns=['Province/State',
                           'Lat', 'Long']).groupby('Country/Region').agg('sum')
    lastdate = df.columns[-1]
    print(f' Data through {lastdate}')
    dfs = df.sort_values(by=lastdate, ascending=False)[:topn].T
    dfs.index = pd.to_datetime(dfs.index)
    return(dfs)

dfs = []

for datafile in datafiles:
    print('Reading', datafile)
    dfs.append(readdf(datafile))
    
titles = ['Cases', 'Deaths', 'Recovered']

def plotdf(df, show=True, save=True, title='test.png',
           plotfrom=plotfrom, topn=topn):
    dateto = str(df.T.columns[-1])[:10]
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    ax[0].set_title(f'{title}')
    df[plotfrom:].plot(lw=3, ax=ax[0], color='green')
    ax[1].set_title(f'New {title}')
    df.diff(1)[plotfrom:].plot(lw=3, ax=ax[1], legend=False, color='green')
    if show: plt.show()
    if save: plt.savefig(f'{title}_{plotfrom}_to_{dateto}_top_{topn}.png')

print(f'Writing charts for top {topn} countries')
for i, title in enumerate(titles):
    plotdf(dfs[i], show=False, title=title)
    



