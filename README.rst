pyreadline
==========

Introduction
============

Pyreadline is a package inspired by GNU readline which aims to improve the
command line editing experience. In most UNIX based pythons GNU readline is
available and used by python but on windows this is not the case. A readline
like python library can also be useful when implementing commandline like
interfaces in GUIs. The use of pyreadline for anything but the windows
console is still under development.

It is based on the UNC readline package by Gary Bishop which in turn is
based on the `ctypes` module in the standard library.

It is not complete. It has been tested for use with Windows 2000 and Windows XP
as well as Windows 10.

Version 2.0 runs on Python 2.6, 2.7, and 3+ using the same code.

Installation
=============

The pyreadline package is based on the readline package by Gary Bishop. It is
not a complete replacement for GNU readline. The pyreadline package is
currently only for the win32 platform. The pyreadline package tries to improve
the integration with the win32 platform by including such things as copy
paste.


Dependencies
------------

  * PyWin32, the win32 Python extensions from
    http://starship.python.net/crew/mhammond.

  * This in turn requires Tomas Heller's ctypes from
    http://starship.python.net/crew/theller/ctypes.


Current release version
-----------------------

Get the installer for the current installer at https://pypi.python.org/pypi/pyreadline/


Development version
-------------------

The development is hosted at https://github.com/pyreadline/pyreadline

The current trunk version can be cloned with git, :command:`git clone
https://github.com/pyreadline/pyreadline.git`.

Install with the usual :command:`python setup.py install` from the pyreadline
folder.


Features
========

*  Keybindings in accordance with the GNU readline library

*  :kbd:`Shift`-Arrow keys for text selection

*  :kbd:`Control-C` for copy

   * Activate with `allow_ctrl_c(True)` in config file. An example is given at
     :file:`pyreadline/configuration/pyreadlineconfig.ini`

*  Double tapping :kbd:`Control-C` will raise a `KeyboardInterrupt`

   * use `ctrl_c_tap_time_interval(x)` where x is your preferred tap time window

   * default 0.3s

*  standard `paste` which pastes first line of content on clipboard

*  Alternatively, users can set the option ``IPython_paste``

   * which pastes tab-separated data as list of lists or numpy array if all data is numeric

*  `paste_multiline_code` pastes code that spans multiple lines or has
   embedded newlines in it.

   * Useful for copy pasting code

The latest development version is always available at the GitHub `repository`_.

.. _repository: https://github.com/pyreadline/pyreadline

.. _history:

History
-------

The pyreadline package is based on the ctypes based UNC readline package by Gary Bishop.


pyreadline copyright and licensing notes
========================================

Unless indicated otherwise, files in this project are covered by a BSD-type
license, included below.

Individual authors are the holders of the copyright for their code and are
listed in each file.

Some files may be licensed under different conditions. Ultimately each file
indicates clearly the conditions under which its author/authors have
decided to publish the code.


pyreadline license
------------------

pyreadline is released under a BSD-type license.

Copyright (c) 2006 J�rgen Stenarson <jorgen.stenarson@bostream.nu>.

Copyright (c) 2003-2006 Gary Bishop

Copyright (c) 2003-2006 Jack Trainor

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

  c. Neither the name of the copyright holders nor the names of any
     contributors to this software may be used to endorse or promote products
     derived from this software without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
