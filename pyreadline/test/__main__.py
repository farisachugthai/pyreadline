#!/usr/bin/env python
# -*- coding: utf-8 -*-
import doctest
import logging
import sys
import unittest
import warnings
from unittest.runner import TextTestRunner
from unittest.suite import TestSuite

logging.basicConfig()

try:
    import pytest
except ImportError:
    warnings.warn("No Pytest. Using unittest.")
    pytest = None


def main():
    dt_suite = doctest.DocTestSuite(test_finder=doctest.DocTestFinder(recurse=True))
    dt_suite.countTestCases()
    dt_suite.debug()
    if pytest is None:
        suite = TestSuite()
        all_test_suites = unittest.defaultTestLoader.discover(start_dir="test")
        suite.addTests(tests=[all_test_suites, dt_suite])
        logging.debug(vars(suite))
        successful = (TextTestRunner().run(suite).wasSuccessful())
        return 0 if successful else 1
    else:
        pytest.main(plugins=[])


if __name__ == '__main__':
    sys.exit(main())
