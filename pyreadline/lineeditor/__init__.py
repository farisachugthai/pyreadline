from __future__ import print_function, unicode_literals, absolute_import

import os
import traceback

from . import lineobj


def _permission_wrapper(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except OSError as e:
        traceback.print_exc(e)
    except PermissionError:
        raise


def touch(filename):
    basedir = os.path.dirname()
    if not os.path.exists(basedir):
        _permission_wrapper(os.makedirs, basedir)
    with open(filename, "ab"):
        _permission_wrapper(os.utime, filename, None)
