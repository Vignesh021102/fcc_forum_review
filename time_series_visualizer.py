import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import df (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean df
df = df[((df['value'] > df['value'].quantile(0.025))&(df['value'] < df['value'].quantile(0.975)))]






monthLabel = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
yearLabel = ["2016","2017","2018","2019"]
fullmonthLabel =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
df['month'] = np.array([x.month for x in df['date']])
df['year'] = np.array([x.year for x in df['date']])

yearBox = [i[1]['value'].values for i in df.groupby('year')]
monthBox = [i[1]['value'].values for i in df.groupby('month')]


def draw_line_plot():
    dateindex = np.arange(0,df.shape[0],round(df.shape[0]/8))
    xtickData = df.iloc[dateindex]['date'].apply(lambda x: f'{x.year}-{x.month:02d}')
    
    fig,ax = plt.subplots(1,1,figsize=(20,8))
    ax.plot(df.index,df['value'],c='red')
    ax.set(title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',ylabel= 'Page Views',xlabel='Date')
    ax.set_xticks(dateindex,xtickData)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    pos = []
    val = []
    brwidth = 5
    fig,ax = plt.subplots(1,1,figsize=(15,10))
    for i,data in df.groupby('month'):
        #print(i)
        val = [j[1]['value'].mean()/1000 for j in data.groupby('year')]
        pos = [(((j[0]-2016)*(brwidth*15))+i*brwidth) for j in data.groupby('year')]
        if len(val) == 3:
          val.insert(0,0)
          pos.insert(0,(i*brwidth))
        ax.bar(pos,val,width=brwidth)
    ax.set(title='',xlabel='Years',ylabel = 'Average Page Views')
    yearPos = np.arange(0,4)*(brwidth*15)+(6*brwidth)
    ax.set_xticks(yearPos,yearLabel)
    ax.legend(fullmonthLabel,title='Months')
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
  fig,ax = plt.subplots(1,2,figsize=(20,10))
  sns.boxplot(ax = ax[0],data = yearBox,notch=True)
  ax[0].set_xticks(np.arange(0,4),yearLabel)
  ax[0].set(title='Year-wise Box Plot (Trend)',ylabel='Page Views',xlabel='Year')

  sns.boxplot(ax = ax[1],data = monthBox,notch=True)
  ax[1].set_xticks(np.arange(0,12),monthLabel)
  ax[1].set(title='Month-wise Box Plot (Seasonality)',ylabel='Page Views',xlabel='Month')
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
