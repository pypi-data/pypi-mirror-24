
'VisiData: a curses interface for exploring and arranging tabular data'

from .vdtui import __version__
from .vdtui import *
from .help import *
from .async import *
from .status_history import *
from .zscroll import *
from .data import *

from .addons.freqtbl import *
from .addons.pyobj import *
from .addons.metasheets import *
from .addons.pivot import *
from .addons.tidydata import *
from .addons.editlog import *
from .addons.freeze import *
from .addons.regex import *

from .addons.csv import *
from .addons.zip import *
from .addons.xlsx import *
from .addons.hdf5 import *
from .addons.sqlite import *

addGlobals(globals())
