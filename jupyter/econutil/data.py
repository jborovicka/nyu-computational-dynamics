# make sure the following libraries are installed
# !pip install --upgrade pandas-datareader
# !pip install --upgrade yfinance

# import necessary libraries
import pandas as pd
import pandas_datareader as pdr
import numpy as np
#from scipy import stats
#from scipy import optimize
#import matplotlib.pyplot as plt
#from matplotlib.patches import Rectangle
#import matplotlib.ticker as ticker
#from io import BytesIO
#import requests
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
# load data from FRED database
def LoadDataFRED(series,transform='none',start = datetime.datetime(1800,1,1),end = datetime.datetime(2050,1,1)):
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
    
# ------------------------------------------------------------------------------
# a slight modification of the OECDReader that allows the specification of
# dataset/series, instead of just a complete dataset
# download via CSV
# example: NAAG/.B9S13S for URL https://stats.oecd.org/SDMX-JSON/data/NAAG/.B9S13S/all
#          SNA_TABLE1/.B1_GA. for URL https://stats.oecd.org/SDMX-JSON/data/SNA_TABLE1/.B1_GA./all
# SSL bug solved with the help of Humphrey Yang

import ssl
import urllib.request

def OECDReaderSeriesCSV(sdmx_query):
    url = f"https://stats.oecd.org/sdmx-json/data/{sdmx_query}&contentType=csv"
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4

    response = urllib.request.urlopen(url, context=ctx)

    return pd.read_csv(response)

# ------------------------------------------------------------------------------
# an updated version of the OECDReader, up to date 2024
# download via CSV
# API definition: https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf
# SDMX API version 1
# https://sdmx.oecd.org/public/rest/data/<agency identifier>,<dataflow identifier>,<dataflow version>/<filter expression>[?<optional parameters>]
# SDMX API version 2
# https://sdmx.oecd.org/public/rest/v2/data/dataflow/<agency identifier>/<dataflow identifier>/<dataflow version>/<filter expression>[?<optional parameters>]

# inputs (for details, see API definition):
#   agency = The identifier of the agency owning the dataflow to be queried., e.g., 'OECD.SDD.NAD'
#   dataflow = The identifier of the dataflow to be queried., e.g., 'DSD_NAAG_VI@DF_NAAG_EXP'
#   version = The version of the dataflow to be queried., e.g., '1.0'
#   filter = The filter expression to be applied to the dataflow., e.g., 'A..B9S13..PT_B1GQ.'
#       obtainable by finding the particular table of interest at https://data-explorer.oecd.org/ and then clicking on the 'Developer API' button
#   startPeriod = The start period of the data to be queried., e.g., '2000' (data from the beginning if empty)
#   endPeriod = The end period of the data to be queried., e.g., '2023' (data to latest if empty)
#   dimensionAtObservation = The dimension at which the observation is made., e.g., 'TIME_PERIOD' / 'AllDimensions'
#   format = The format of the data to be returned., e.g., 'csvfile' / 'csvfilewithlabels' (the latter includes the dimension verbose labels, not just identifiers)

def OECDReaderSeriesCSV2(dataflow,filter,agency='OECD.SDD.NAD',version='1.0',startPeriod='',endPeriod='',dimensionAtObservation='AllDimensions',format='csvfile'):
    if startPeriod == '':
        startPeriodtext = ""
    else:
        startPeriodtext = f"&startPeriod={startPeriod}"
    if endPeriod == '':
        endPeriodtext = ""
    else:
        endPeriodtext = f"&endPeriod={endPeriod}"

    url = f"https://sdmx.oecd.org/public/rest/data/{agency},{dataflow},{version}/{filter}?dimensionAtObservation={dimensionAtObservation}{startPeriodtext}{endPeriodtext}&format={format}"
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4

    response = urllib.request.urlopen(url, context=ctx)

    return pd.read_csv(response)
