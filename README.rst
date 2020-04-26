==========
pyreadline
==========

The pyreadline package is a python implementation of GNU readline functionality.

It is based on the UNC readline package by Gary Bishop which in turn is
based on the `ctypes` module in the standard library.

It is not complete. It has been tested for use with Windows 2000 and Windows XP
as well as Windows 10.

Version 2.0 runs on Python 2.6, 2.7, and 3+ using the same code.

Features:

*  Keyboard text selection and copy/paste
*  Shift-Arrow keys for text selection
*  Control-c can be used for copy. Activate with `allow_ctrl_c(True)` in config file
   `pyreadlineconfig.ini`.
*  Double tapping Ctrl-C will raise a `KeyboardInterrupt`
   * use `ctrl_c_tap_time_interval(x)` where x is your preferred tap time window
   * default 0.3s
*  standard `paste` which pastes first line of content on clipboard.
*  IPython_paste, which pastes tab-separated data as list of lists
   or numpy array if all data is numeric
*  `paste_multiline_code` pastes code that spans multiple lines or has
   embedded newlines in it.
   * Useful for copy pasting code

The latest development version is always available at the GitHub `repository`_.

.. _repository: https://github.com/pyreadline/pyreadline

