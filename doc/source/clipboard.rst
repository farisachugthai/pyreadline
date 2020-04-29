=========
Clipboard
=========

Pyreadline can do copy/paste using the clipboard. Selections can be done using
shift and arrowkeys as in most windows programs.

There are three different paste functions that can be bound.:

.. glossary::

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


Clipboard API
==============

.. automodule:: pyreadline.clipboard
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.clipboard.ironpython_clipboard
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.clipboard.no_clipboard
   :members:
   :undoc-members:
   :show-inheritance:


.. automodule:: pyreadline.clipboard.win32_clipboard
   :members:
   :undoc-members:
   :show-inheritance: