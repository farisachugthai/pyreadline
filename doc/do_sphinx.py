#!/usr/bin/env python
"""Script to build documentation using Sphinx.
"""
from __future__ import print_function

import fileinput
import os
import shlex
import sys

try:
    from subprocess import run
except ImportError:
    run = None

try:
    from runpy import run_module
except ImportError:
    run_module = None

def oscmd(c):
    if run is not None:
        cmd = [sys.executable, '-m'].extend(shlex.split(shlex.quote(c)))
        return run(cmd)
    else:
        os.system(c)


def main():
    # html manual.
    oscmd("sphinx-build -d build/doctrees source build/html")

    if sys.platform == "win32":
        return

    # LaTeX format.
    oscmd("sphinx-build -b latex -d build/doctrees source build/latex")

    # Produce pdf.
    topdir = os.getcwd()
    os.chdir("build/latex")

    # Change chapter style to section style: allows chapters to start on
    # the current page.  Works much better for the short chapters we have.
    # This must go in the class file rather than the preamble, so we modify
    # manual.cls at runtime.
    chapter_cmds = r"""
% Local changes.
\renewcommand\chapter{
    \thispagestyle{plain}
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter
}
\def\@makechapterhead#1{
    \vspace*{10\p@}
    {\raggedright \reset@font \Huge \bfseries \thechapter \quad #1}
    \par\nobreak
    \hrulefill
    \par\nobreak
    \vspace*{10\p@}
}
\def\@makeschapterhead#1{
    \vspace*{10\p@}
    {\raggedright \reset@font \Huge \bfseries #1}
    \par\nobreak
    \hrulefill
    \par\nobreak
    \vspace*{10\p@}
}
"""

    unmodified = True
    for line in fileinput.FileInput("manual.cls", inplace=1):
        if "Support for module synopsis" in line and unmodified:
            line = chapter_cmds + line
        elif "makechapterhead" in line:
            # Already have altered manual.cls: don't need to again.
            unmodified = False
        print(line)

    # Copying the makefile produced by sphinx...
    oscmd("pdflatex pyreadline.tex")
    oscmd("pdflatex pyreadline.tex")
    oscmd("pdflatex pyreadline.tex")
    oscmd("makeindex -s python.ist pyreadline.idx")
    oscmd("makeindex -s python.ist modpyreadline.idx")
    oscmd("pdflatex pyreadline.tex")
    oscmd("pdflatex pyreadline.tex")

    # Create a manual/ directory with final html/pdf output
#    os.chdir(topdir)
#    oscmd('rm -rf manual')
#    oscmd('mkdir manual')
#    oscmd('cp -r build/html/*.html build/html/_static manual/')
#    oscmd('cp build/latex/ipython.pdf manual/')

if __name__ == '__main__':
    if run_module is None:
        main()
    else:
        run_module('sphinx', init_globals=globals())
