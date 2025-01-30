

# read version from installed package
import importlib
try:
    importlib.import_module('econutil')
    # from importlib.metadata import version
    __version__ = importlib.metadata.version("econutil")
except ImportError:
    __version__ = "n/a - local"

# import modules from the folder    
#from .defs import *
#from .datasources import *
#from .plot import *

from econutil.defs import *
from econutil.data import *
from econutil.plot import *
# from .defs import *

print('Root package econutil imported.')
