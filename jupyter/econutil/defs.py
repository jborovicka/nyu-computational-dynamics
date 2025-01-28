# import necessary libraries
import numpy as np

# ==============================================================================
# recession dates and plotting recessions 
NBERRecessionDates = np.array([
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

myNBERRecessionQuarters = np.array([
  [18573,18584],
  [18604,18613],
  [18652,18681],
  [18693,18704],
  [18734,18791],
  [18822,18852],
  [18873,18881],
  [18904,18912],
  [18932,18942],
  [18961,18972],
  [18994,19004],
  [19031,19043],
  [19073,19082],
  [19102,19114],
  [19132,19144],
  [19184,19191],
  [19202,19213],
  [19233,19243],
  [19264,19274],
  [19294,19331],
  [19373,19382],
  [19452,19454],
  [19491,19494],
  [19533,19542],
  [19574,19582],
  [19603,19611],
  [19701,19704],
  [19741,19751],
  [19802,19803],
  [19814,19824],
  [19904,19911],
  [20012,20014],
  [20081,20092],
  [20201,20202]])

myNBERRecessionMonths = np.array([
  [185707,185812],
  [186011,186106],
  [186505,186712],
  [186907,187012],
  [187311,187903],
  [188204,188505],
  [188704,188804],
  [189008,189105],
  [189302,189406],
  [189601,189706],
  [189907,190012],
  [190210,190408],
  [190706,190806],
  [191002,191201],
  [191302,191412],
  [191809,191903],
  [192002,192107],
  [192306,192407],
  [192611,192711],
  [192909,193303],
  [193706,193806],
  [194503,194510],
  [194812,194910],
  [195308,195405],
  [195709,195804],
  [196005,196102],
  [197001,197011],
  [197312,197503],
  [198002,198007],
  [198108,198211],
  [199008,199103],
  [200104,200111],
  [200801,200906],
  [202003,202004]])

# create recession dummies using myNBERRecessionMonths and myNBERRecessionQuarters
# for quarters, use interval = [YYYYQ begin, YYYYQ end]
# for months, use interval = [YYYYMM begin, YYYYMM end]
def CreateRecessionDummies(interval):
    
    if interval[0]>99999:
        # months
        divisor,periods = 100,12
        recessions = np.append(myNBERRecessionMonths,[[999999,999999]],axis=0)
    else:
        # quarters
        divisor,periods = 10,4
        recessions = np.append(myNBERRecessionQuarters,[[999999,999999]],axis=0)
    
    T = periods*(interval[1]//divisor - interval[0]//divisor) + interval[1]%divisor - interval[0]%divisor + 1
    period_ids = np.zeros(T,dtype=np.int32)
    dummies = np.zeros(T,dtype=np.int32)
    indices = np.where(recessions[:,1] >= interval[0])
    ind = indices[0][0]
    y,q = interval[0]//divisor, interval[0]%divisor
    t = 0
    while t < T:
        period_ids[t] = y*divisor+q
        if recessions[ind,0] <= y*divisor+q:
            dummies[t] = 1
        q += 1
        if q==periods+1:
            q = 1
            y += 1
        if recessions[ind,1] < y*divisor+q:
            ind += 1
        t += 1

    return period_ids, dummies 

# ==============================================================================
# color definitions as in Paul Tol's set
# https://personal.sron.nl/~pault/

tolColor = dict(
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
clist_vibrant = [tolColor['tolVibrantBlue'],
                 tolColor['tolVibrantOrange'],
                 tolColor['tolVibrantCyan'],
                 tolColor['tolVibrantMagenta'],
                 tolColor['tolVibrantTeal'],
                 tolColor['tolVibrantRed'],
                 tolColor['tolVibrantGrey'],
                 tolColor['tolBrightYellow']]