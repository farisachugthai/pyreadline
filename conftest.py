import linecache
import multiprocessing
import sys
from warnings import simplefilter

import pytest

simplefilter("ignore", category=DeprecationWarning)
simplefilter("ignore", category=PendingDeprecationWarning)

linecache.clearcache()


def pytest_load_initial_conftests(args):
    """If you have the xdist plugin installed you will now always perform test runs using a number of subprocesses close to your CPU."""
    if "xdist" in sys.modules:  # pytest-xdist plugin

        num = max(multiprocessing.cpu_count() / 2, 1)
        args[:] = ["-n", str(num)] + args


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({})".format(previousfailed.name))

