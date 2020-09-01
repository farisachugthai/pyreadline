from __future__ import print_function, unicode_literals, absolute_import

import glob
import sys

from pyreadline.error import ConsoleError

success = False
in_ironpython = "IronPython" in sys.version

if in_ironpython:
    try:
        #         from .ironpython_console import *
        from .ironpython_console import install_readline
    except ImportError:
        raise
    else:
        success = True
else:
    try:
        #         from .console import *
        from .console import install_readline

        success = True
    except ImportError:
        raise

if not success:
    raise ConsoleError
