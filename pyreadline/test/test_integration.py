#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the integration test file from pdbpp.

I wanted some integration tests from another python/REPL/command-line project.
This'll serve as good inspiration.
"""
import sys

import pytest
from _pytest.fixtures


def test_integration(testdir, readline_param):
    tmpdir = testdir.tmpdir

    f = tmpdir.ensure("test_file.py")
    f.write("print('before'); __import__('pdb').set_trace(); print('after')")

    if readline_param != "pyrepl":
        # Create empty pyrepl module to ignore any installed pyrepl.
        mocked_pyrepl = tmpdir.ensure("pyrepl.py")
        mocked_pyrepl.write("")

    child = testdir.spawn(sys.executable + " test_file.py", expect_timeout=1)
    child.expect_exact("\n(Pdb++) ")

    if readline_param != "pyrepl":
        # Remove it after startup to not interfere with completions.
        mocked_pyrepl.remove()

    if readline_param == "pyrepl":
        child.expect_exact("\x1b[?12l\x1b[?25h")
        pdbpp_prompt = "\n(Pdb++) \x1b[?12l\x1b[?25h"
    else:
        pdbpp_prompt = "\n(Pdb++) "

    # Completes help as unique (coming from pdb and fancycompleter).
    child.send(b"hel\t")
    if readline_param == "pyrepl":
        child.expect_exact(b"\x1b[1@h\x1b[1@e\x1b[1@l\x1b[1@p")
    else:
        child.expect_exact(b"help")
    child.sendline("")
    child.expect_exact("\r\nDocumented commands")
    child.expect_exact(pdbpp_prompt)

    # Completes breakpoints via pdb, should not contain "\t" from
    # fancycompleter.
    if sys.version_info >= (3, 3):
        child.send(b"b \t")
        if readline_param == "pyrepl":
            child.expect_exact(b'\x1b[1@b\x1b[1@ \x1b[?25ltest_file.py:'
                               b'\x1b[?12l\x1b[?25h')
        else:
            child.expect_exact(b'b test_file.py:')

        child.sendline("")
        if readline_param == "pyrepl":
            child.expect_exact(
                b"\x1b[23D\r\n\r\x1b[?1l\x1b>*** Bad lineno: \r\n"
                b"\x1b[?1h\x1b=\x1b[?25l\x1b[1A\r\n(Pdb++) \x1b[?12l\x1b[?25h"
            )
        else:
            child.expect_exact(b"\r\n*** Bad lineno: \r\n(Pdb++) ")

    child.sendline("c")
    rest = child.read()
    if readline_param == "pyrepl":
        assert rest == b'\x1b[1@c\x1b[9D\r\n\r\x1b[?1l\x1b>'
    else:
        assert rest == b'c\r\n'
