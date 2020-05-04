=====
Usage
=====

.. currentmodule:: pyreadline.configuration.pyreadlineconfig

The purpose of readline is to improve the interactive experience with the
python interpreter by improving the line editing facilities. The most important
being tab completion and copy and paste.

Configuration files
===================

Examples of Configuration Files
================================

Here is the example config file shipped with pyreadline:

.. literalinclude:: ../../pyreadline/configuration/pyreadlineconfig.ini


Example with Callbacks
----------------------

.. include:: ../../pyreadline/examples/callback_example.py
   :code: python


Example with Tk
----------------------

.. include:: ../../pyreadline/examples/tk_gui.py
   :code: python


API for Config File
===================

.. automodule:: pyreadline.configuration
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.configuration.startup
   :members:
   :undoc-members:
   :show-inheritance:


Valid Keys --- Mappings chars to the physical keys.
===================================================

pyreadline considers any key in the following set to be valid.


Things to Keep in Mind
-----------------------

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

Any code in a file pointed to by `PYTHONSTARTUP` is automatically executed
when the interpreter detects that it's being run in interactive mode.

However, readline is automatically imported by the `site` module which is
enabled by default. As a result, this environment variable doesn't need
to be defined.


pyreadline with IronPython
--------------------------

*THIS HAS NOT BEEN TESTED FOR A WHILE*

Pyreadline can be used together with IronPython. Unfortunately the binary
installs of IronPython can not run pyreadline directly. You need to patch the
source code to make ``PythonCommandLine`` a public class that we can override.

* In ``PythonCommandLine.cs`` you need to change class ``PythonCommandLine`` to public
  class ``PythonCommandLine`` and recompile.

* Copy rlcompleter.py from a standard python install to your IronPython path
  (this file is not included with fepy).


International characters
------------------------

The pyreadline package now supports international characters.

This can refer to many sets of characters, including "double-wide" characters,
and more generally, sets of letters in encodings other than the UTF-8 standard that
the interpreter assumes.

However, using international characters in the interactive prompt can be annoying on windows
since the default codepage for the terminal is an ascii codepage (850 on
Swedish systems) but the filesystem often uses some other codepage (1252 on
Swedish systems). This means the filenames containing international characters
entered on interactive prompt will not work. The workaround here is to change
the codepage of your terminal to a more suitable one using the :command:`chcp`
command. For Swedish systems :command:`chcp 1252` does the trick but you also
have to change the terminal font to a font compatible with the wanted code page
in the case of a Swedish system that would be e.g. ``Lucida Console``, or
``Consolas`` using the properties dialog for the console.
