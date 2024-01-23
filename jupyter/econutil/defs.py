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