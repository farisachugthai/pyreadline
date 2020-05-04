"""Establish python2/python3 compatibility.

.. data:: PY3

    Bool

.. function:: callable(x)

    isinstance(x, collections.abc.Callable)

.. function:: execfile(fname, glob=None, loc=None)

    execfile as per python2 builtins.

"""

from __future__ import print_function, unicode_literals, absolute_import
import sys

if sys.version_info[0] >= 3:
    # TODO: if sys.version_info < (3,6): class ModuleNotFoundError(ImportError)

    from builtins import str, bytes

    # bytes = bytes
    from io import StringIO, open
    import collections

    PY3 = True

    def callable(x):
        return isinstance(x, collections.abc.Callable)

    def execfile(fname, glob=None, loc=None):
        glob = glob if glob is not None else globals()
        loc = loc if loc is not None else locals()
        with open(fname, "rb") as fil:
            txt = fil.read()
            try:
                code_obj = compile(txt, fname, "exec")
            except Exception:
                raise
            try:
                exec(code_obj, glob, loc)
            except Exception:
                raise

    unicode = str
else:
    from builtins import callable, execfile, unicode, str
    from StringIO import StringIO

    PY3 = False
    # callable = callable
    # execfile = execfile
    # unicode = unicode

    # Wtf??
    bytes = str
