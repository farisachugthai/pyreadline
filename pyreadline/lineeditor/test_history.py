#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest

from .history import HistoryFile, LineHistory, OrderedHistory  # noqa


# def test_line_history():
#     assert False


@pytest.mark.usefixtures("tmpdir")
class TestHistoryFile:

    # more for pytest than anything but w/e
    def test_cwd_starts_empty(self, tmpdir):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self, tmpdir):
        assert os.listdir(os.getcwd()) == []

    def test_difference_between_marker_and_parameter(self, tmpdir):
        print(dir(tmpdir))
        assert tmpdir

    def test_tmpdir_as_parameter(self, tmpdir):
        print(dir(tmpdir))
        assert tmpdir

    def test_init_history_file(self, tmpdir):
        print('*****What is the pytest tmpdir dir again?')
        print(dir(tmpdir))

        assert HistoryFile(tmpdir)


# def test_ordered_history():
#     assert False

if __name__ == '__main__':
    pytest.main()
