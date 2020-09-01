from __future__ import print_function, unicode_literals, absolute_import

import traceback
import sys
from . import winconstants  # noqa

in_ironpython = "IronPython" in sys.version

if in_ironpython:
    try:
        from .ironpython_keysyms import *

        success = True
    except ImportError:
        raise
else:
    if sys.platform.startswith("Win"):
        try:
            from .keysyms import *

            success = True
        except ImportError:
            # raise ImportError("Could not import: %s" % x)
            traceback.print_exception(*x)
    else:
        sys.exit("This is a Windows only program. Comment me out if you want but...")
