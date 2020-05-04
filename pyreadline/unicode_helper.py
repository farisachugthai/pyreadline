# -*- coding: utf-8 -*-
"""Unicode Aides.

.. data:: pyreadline_codepage

   Normally the codepage for pyreadline is set to be locale.getpreferredencoding

   If you need to change this, you can put the following lines in a file pointed
   to by `PYTHONSTARTUP`:

      import pyreadline
      pyreadline.unicode_helper.pyreadline_codepage="utf8"

   Note that this startupfile *would* be in contrast to the pyreadineconfig.ini.

"""
# *****************************************************************************
#       Copyright (C) 2007  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
import codecs
import locale
import sys

from pyreadline.py3k_compat import unicode, bytes

try:
    pyreadline_codepage = locale.getpreferredencoding()
except AttributeError:
    # This error occurs when pdb imports readline and doctest has replaced
    # stdout with stdout collector.
    pyreadline_codepage = "ascii"

if pyreadline_codepage is None:
    pyreadline_codepage = "ascii"

if sys.version_info < (2, 6):
    bytes = str

PY3 = sys.version_info >= (3, 0)


def ensure_unicode(text):
    """helper to ensure that text passed to WriteConsoleW is unicode"""
    if isinstance(text, bytes):
        try:
            return text.decode(pyreadline_codepage, "replace")
        except (LookupError, TypeError, UnicodeDecodeError):
            return text.decode("ascii", "replace")
    # uncomment for pain. holy fuck the number of times this unction
    # is simply called incorrectly...
    # else:
    #     raise TypeError
    return text


def ensure_str(text):
    """Convert unicode to str using pyreadline_codepage"""
    try:
        return codecs.encode(text, encoding=pyreadline_codepage, errors="replace")
    except (LookupError, TypeError, UnicodeEncodeError):
        return codecs.encode(text, encoding="ascii", errors="replace")
    return text


def biter(text):
    # bytes iter. it took me a minute too
    if PY3 and isinstance(text, bytes):
        return (s.to_bytes(1, "big") for s in text)
    else:
        return iter(text)
