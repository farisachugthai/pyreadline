=====
Usage
=====

The purpose of readline is to improve the interactive experience with the
python interpreter by improving the line editing facilities. The most important
being tab completion and copy and paste.

pyreadline with IronPython
--------------------------

*THIS HAS NOT BEEN TESTED FOR A WHILE*

Pyreadline can be used together with IronPython. Unfortunately the binary
installs of IronPython can not run pyreadline directly. You need to patch the
source code to make PythonCommandLine a public class that we can override.

* In PythonCommandLine.cs you need to change class PythonCommandLine to public
  class PythonCommandLine and recompile.

* Copy rlcompleter.py from a standard python install to your ironpython path
  (this file is not included with fepy).


Clipboard
---------

Pyreadline can do copy/paste using the clipboard. Selections can be done using
shift and arrowkeys as in most windows programs.

There are three different paste functions that can be bound.


    paste
      Paste windows clipboard. Assume single line strip other lines and end of
      line markers and trailing spaces

    paste_mulitline_code
      Paste windows clipboard as multiline code. Removes any empty lines in the
      code

    ipython_paste
      Paste windows clipboard. If enable_ipython_paste_list_of_lists is True
      then try to convert tabseparated data to repr of list of lists or repr of
      array. If enable_ipython_paste_for_paths==True then change \\\\ to / and
      spaces to \\space.


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


Example of a Configuration File
===============================

Here is the example config file shipped with pyreadline:

.. literalinclude:: ../../pyreadline/configuration/pyreadlineconfig.ini

