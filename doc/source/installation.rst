===================================
Install instructions for pyreadline
===================================

The pyreadline package is based on the readline package by Gary Bishop. It is
not a complete replacement for GNU readline. The pyreadline package is
currently only for the win32 platform. The pyreadline package tries to improve
the integration with the win32 platform by including such things as copy
paste.


Dependencies
============

  * PyWin32, the win32 Python extensions from
    http://starship.python.net/crew/mhammond.

  * This in turn requires Tomas Heller's ctypes from
    http://starship.python.net/crew/theller/ctypes.



Current release version
=======================

Get the installer for the current installer at
https://pypi.python.org/pypi/pyreadline/

Follow the instructions for configuration below.

Development version
===================

The development is hosted at https://github.com/pyreadline/pyreadline

The current trunk version can be cloned with git, :command:`git clone
https://github.com/pyreadline/pyreadline.git`.

Install with the usual :command:`python setup.py install` from the pyreadline
folder.

Follow the instructions for configuration below.

Configuration files
===================

There are a few things that are not automatically installed.

*  Copy ``pyreadlineconfig.ini`` from
   :file:`../../pyreadline/configuration/pyreadlineconfig.ini`
   to your `HOME` directory (usually ``C:/Documents and Settings/YOURNAME``
   or ``C:\Users\Username``).

   * Alternatively, one can define the HOME environment variable as so.

.. envvar:: HOMEDRIVE

   Conventionally set to the C: drive.

.. envvar:: HOMEPATH

   The path from the root of the C: drive to the user's home directory.

As such one can define home as the concatenation of `HOMEDRIVE` and `HOMEPATH`.

.. envvar:: HOME

   The user's home directory.


Optional Startup Code
---------------------

If one defines `PYTHONSTARTUP`, add the code in
:file:`../../pyreadline/configuration/startup.py`

Any code in a file pointed to by PYTHONSTARTUP is automatically executed
when the interpreter detects that it's being run in interactive mode. 

However, readline is automatically imported by the `site` module which is
enabled by default. As a result, this environment variable doesn't need
to be defined.
