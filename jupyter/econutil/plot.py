# import necessary libraries
#import pandas as pd
#import pandas_datareader as pdr
#import numpy as np
#from scipy import stats
#from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
#from io import BytesIO
#import requests
#import datetime

from econutil.defs import *

# ==============================================================================
# function definitions

# ------------------------------------------------------------------------------
# time series plot
def GenerateTSPlot(param = {}):
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
                for i in range(NBERRecessionDates.shape[0]):
                    ax[row][col].add_patch(Rectangle((NBERRecessionDates[i,0],p['showNBERrecessions_y'][0]),
                                   NBERRecessionDates[i,1]-NBERRecessionDates[i,0],
                                   p['showNBERrecessions_y'][1]-p['showNBERrecessions_y'][0],
                                   facecolor=tolColor['tolPaleGrey'],zorder=-1))

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
                ax[row][col].grid(which='both',color = tolColor['tolDarkGrey'], linestyle = ':', linewidth = 0.5)
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
def GenerateBarPlot(param = {}):
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
                                   facecolor=tolColor['tolPaleGrey'],zorder=-1))

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
        ax.grid(which='both',color = tolColor['tolDarkGrey'], linestyle = ':', linewidth = 0.5)
    if p['highlightzero']:
        ax.plot(p['xlim'],[0,0],linewidth=1.5,color='#000000',linestyle=':')
    if p['ylogscale']:
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, 
            pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
        ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y,
            pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))

    return fig,ax;
