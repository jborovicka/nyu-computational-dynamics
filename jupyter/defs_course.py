# make sure the following libraries are installed
# !pip install --upgrade pandas-datareader
# !pip install --upgrade yfinance

# import necessary libraries
import pandas as pd
import pandas_datareader as pdr
import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
from io import BytesIO
import requests
import datetime

# ==============================================================================
# function definitions

# ------------------------------------------------------------------------------
# calculation date as a fraction of the year, from a datetime vector
def year_frac(ts):
    yf = np.empty(ts.size)
    for i in range(ts.size):
        days = 365 + ts[i].is_leap_year*1
        yf[i] = ts[i].year + ts[i].dayofyear/days + ts[i].hour/24/days + ts[i].minute/60/24/days + ts[i].second/60/60/24/days
    return yf

# ------------------------------------------------------------------------------
# time series plot
def myLoadDataFRED(series,transform='none',start = datetime.datetime(1800,1,1),end = datetime.datetime(2050,1,1)):
    # work out start and end 
    data = pdr.data.DataReader(series,'fred',start,end)
    d = dict()
    d['orig'] = data
    d['transform'] = transform
    d['year'] = year_frac(ts=data.index)
    d['freq'] = int(round(1/(d['year'][1]-d['year'][0]),0))
    T = len(d['year'])
    for i in series:
        d[i] = data[i].to_numpy()
        if transform=='pct_change_year_ago':
            d[i][d['freq']:T] = (d[i][d['freq']:T] - d[i][0:T-d['freq']]) / d[i][0:T-d['freq']] * 100
            d[i][0:d['freq']] = float('nan')
        
    return d

# ------------------------------------------------------------------------------
# time series plot
def myGenerateTSPlot(param = {}):
    p = {'figsize' : [15,9], 'fontsize': 16, 'subplots': [1,1],
         'title': '',
         'ylim': [0,0],
         'xlabel': '', 'ylabel': '',
         'ylogscale': False,
         'showgrid': False, 'highlightzero': False,
         'showNBERrecessions' : False, 'showNBERrecessions_y': [0,1]}
    # overwrite keys in p using param
    for i in param.keys():
        p[i] = param[i]
    
    plt.rcParams['figure.figsize'] = p['figsize']  # Set default figure size
    plt.rcParams['font.size'] = p['fontsize']      # Set default font size
    fig,ax = plt.subplots(p['subplots'][0],p['subplots'][1],squeeze=False)
    
    for row in range(p['subplots'][0]):
        for col in range(p['subplots'][1]):
                     
            if p['showNBERrecessions']:
                for i in range(myNBERRecessionDates.shape[0]):
                    ax[row][col].add_patch(Rectangle((myNBERRecessionDates[i,0],p['showNBERrecessions_y'][0]),
                                   myNBERRecessionDates[i,1]-myNBERRecessionDates[i,0],
                                   p['showNBERrecessions_y'][1]-p['showNBERrecessions_y'][0],
                                   facecolor=myColor['tolPaleGrey'],zorder=-1))

            if len(p['title']) > 0:
                ax[row][col].set_title(p['title'])
            if p['xlim'][1] > p['xlim'][0]:
                ax[row][col].set_xlim(p['xlim'])
            if p['ylim'][1] > p['ylim'][0]:
                ax[row][col].set_ylim(p['ylim'])
            if len(p['xlabel']) > 0:
                ax[row][col].set_xlabel(p['xlabel'])
            if len(p['ylabel']) > 0:
                ax[row][col].set_ylabel(p['ylabel'])
            if p['showgrid']:
                ax[row][col].grid(which='both',color = myColor['tolDarkGrey'], linestyle = ':', linewidth = 0.5)
            if p['highlightzero']:
                ax[row][col].plot(p['xlim'],[0,0],linewidth=1.5,color='#000000',linestyle=':')
            if p['ylogscale']:
                ax[row][col].set_yscale('log')
                ax[row][col].yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, 
                    pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
                ax[row][col].yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y,
                    pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

    if p['subplots'] == [1,1]:
        ax = ax[0][0];
        
    return fig,ax;

# ------------------------------------------------------------------------------
# bar plot
def myGenerateBarPlot(param = {}):
    p = {'figsize' : [15,9], 'fontsize': 16,
         'title': '',
         'xlim': [0,0], 'ylim': [0,0],
         'xlabel': '', 'ylabel': '',
         'ylogscale': False,
         'showgrid': False, 'highlightzero': False,
         'showNBERrecessions' : False, 'showNBERrecessions_y': [0,1]}
    # overwrite keys in p using param
    for i in param.keys():
        p[i] = param[i]
    
    plt.rcParams['figure.figsize'] = p['figsize']  # Set default figure size
    plt.rcParams['font.size'] = p['fontsize']      # Set default font size
    fig,ax = plt.subplots()
    
    if p['showNBERrecessions']:
        for i in range(myNBERRecessionDates.shape[0]):
            ax.add_patch(Rectangle((myNBERRecessionDates[i,0],p['showNBERrecessions_y'][0]),
                                   myNBERRecessionDates[i,1]-myNBERRecessionDates[i,0],
                                   p['showNBERrecessions_y'][1]-p['showNBERrecessions_y'][0],
                                   facecolor=myColor['tolPaleGrey'],zorder=-1))

    if len(p['title']) > 0:
        ax.set_title(p['title'])
    if p['xlim'][1] > p['xlim'][0]:
        ax.set_xlim(p['xlim'])
    if p['ylim'][1] > p['ylim'][0]:
        ax.set_ylim(p['ylim'])
    if len(p['xlabel']) > 0:
        ax.set_xlabel(p['xlabel'])
    if len(p['ylabel']) > 0:
        ax.set_ylabel(p['ylabel'])
    if p['showgrid']:
        ax.grid(which='both',color = myColor['tolDarkGrey'], linestyle = ':', linewidth = 0.5)
    if p['highlightzero']:
        ax.plot(p['xlim'],[0,0],linewidth=1.5,color='#000000',linestyle=':')
    if p['ylogscale']:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, 
            pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y,
            pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

    return fig,ax;

# ==============================================================================
# a slight modification of the OECDReader that allows the specification of
# dataset/series, instead of just a complete dataset
# example: NAAG/.B9S13S for URL https://stats.oecd.org/SDMX-JSON/data/NAAG/.B9S13S/all
#          SNA_TABLE1/.B1_GA. for URL https://stats.oecd.org/SDMX-JSON/data/SNA_TABLE1/.B1_GA./all

from pandas_datareader.base import _BaseReader
from pandas_datareader.compat import string_types
from pandas_datareader.io import read_jsdmx

class OECDReaderSeries(_BaseReader):
    """Get data for the given name from OECD."""

    _format = "json"

    @property
    def url(self):
        """API URL"""
        url = "https://stats.oecd.org/SDMX-JSON/data"

        if not isinstance(self.symbols, string_types):
            raise ValueError("data name must be string")

        # API: https://data.oecd.org/api/sdmx-json-documentation/
        return "{0}/{1}/all?".format(url, self.symbols)

    def _read_lines(self, out):
        """read one data from specified URL"""
        df = read_jsdmx(out)
        try:
            idx_name = df.index.name  # hack for pandas 0.16.2
            df.index = pd.to_datetime(df.index, errors="ignore")
            for col in df:
                df[col] = pd.to_numeric(df[col], errors="ignore")
            df = df.sort_index()
            df = df.truncate(self.start, self.end)
            df.index.name = idx_name
        except ValueError:
            pass
        return df
    
# ==============================================================================
# recession dates and plotting recessions 
myNBERRecessionDates = np.array([
  [1857.46,1858.96],
  [1860.79,1861.46],
  [1865.29,1867.96],
  [1869.46,1870.96],
  [1873.79,1879.21],
  [1882.21,1885.38],
  [1887.21,1888.29],
  [1890.54,1891.38],
  [1893.04,1894.46],
  [1895.96,1897.46],
  [1899.46,1900.96],
  [1902.71,1904.63],
  [1907.38,1908.46],
  [1910.04,1912.04],
  [1913.04,1914.96],
  [1918.63,1919.21],
  [1920.04,1921.54],
  [1923.38,1924.54],
  [1926.79,1927.88],
  [1929.63,1933.21],
  [1937.38,1938.46],
  [1945.13,1945.79],
  [1948.88,1949.79],
  [1953.54,1954.38],
  [1957.63,1958.29],
  [1960.29,1961.13],
  [1969.96,1970.88],
  [1973.88,1975.21],
  [1980.04,1980.54],
  [1981.54,1982.88],
  [1990.54,1991.21],
  [2001.21,2001.88],
  [2007.96,2009.46],
  [2020.13,2020.29]])

# ==============================================================================
# color definitions as in Paul Tol's set
# https://personal.sron.nl/~pault/

myColor = dict(
# Bright scheme
tolBrightBlue = '#4477AA',
tolBrightCyan = '#66CCEE',
tolBrightGreen = '#228833',
tolBrightYellow = '#CCBB44',
tolBrightRed = '#EE6677',
tolBrightPurple = '#AA3377',
tolBrightGrey = '#BBBBBB',

# High-contrast scheme
tolHighContrastWhite = '#FFFFFF',
tolHighContrastYellow = '#DDAA33',
tolHighContrastRed = '#BB5566',
tolHighContrastBlue = '#004488',
tolHighContrastBlack = '#000000',

# Vibrant scheme
tolVibrantOrange = '#EE7733',
tolVibrantBlue = '#0077BB',
tolVibrantCyan = '#33BBEE',
tolVibrantMagenta = '#EE3377',
tolVibrantRed = '#CC3311',
tolVibrantTeal = '#009988',
tolVibrantGrey = '#BBBBBB',

# Muted scheme
tolMutedRose = '#CC6677',
tolMutedIndigo = '#332288',
tolMutedSand = '#DDCC77',
tolMutedGreen = '#117733',
tolMutedCyan = '#88CCEE',
tolMutedWine = '#882255',
tolMutedTeal = '#44AA99',
tolMutedOlive = '#999933',
tolMutedPurple = '#AA4499',
tolMutedPaleGrey = '#DDDDDD',

# Pale and Dark Schemes
tolPaleBlue = '#BBCCEE',
tolPaleCyan = '#CCEEFF',
tolPaleGreen = '#CCDDAA',
tolPaleYellow = '#EEEEBB',
tolPaleRed = '#FFCCCC',
tolPaleGrey = '#DDDDDD',
tolDarkBlue = '#222255',
tolDarkCyan = '#225555',
tolDarkGreen = '#225522',
tolDarkYellow = '#666633',
tolDarkRed = '#663333',
tolDarkGrey = '#555555',

# Light scheme
tolLightBlue = '#77AADD',
tolLightCyan = '#99DDFF',
tolLightMint = '#44BB99',
tolLightPear = '#BBCC33',
tolLightOlive = '#AAAA00',
tolLightYellow = '#EEDD88',
tolLightOrange = '#EE8866',
tolLightPink = '#FFAABB',
tolLightGrey = '#DDDDDD',

# Medium Contrast scheme
tolMediumContrastWhite = '#FFFFFF',
tolMediumContrastLightYellow = '#EECC66',
tolMediumContrastLightRed = '#EE99AA',
tolMediumContrastLightBlue = '#6699CC',
tolMediumContrastDarkYellow = '#997700',
tolMediumContrastDarkRed = '#994455',
tolMediumContrastDarkBlue = '#004488',
tolMediumContrastBlack = '#000000'
)

# ==============================================================================
# color lists
clist_1 = [myColor['tolVibrantBlue'],
           myColor['tolVibrantOrange'],
           myColor['tolVibrantCyan'],
           myColor['tolVibrantMagenta'],
           myColor['tolVibrantTeal'],
           myColor['tolVibrantRed'],
           myColor['tolVibrantGrey'],
           myColor['tolBrightYellow']]