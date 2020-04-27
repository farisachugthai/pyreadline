# -*- coding: utf-8 -*-
"""Release data for the pyreadline project.

$Id$

Previously was held at pyreadline/release.py.
"""

# *****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@kroywen.se>
#
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

# *****************************************************************************
#       Copyright (C) 2003-2006 Gary Bishop.
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

import codecs
import glob
import logging
import os
import sys
from platform import system

logging.basicConfig()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

    find_packages = None
else:
    from setuptools import find_packages

try:
    import sphinx
except ImportError:
    cmd_class = {}
else:
    from sphinx.setup_command import BuildDoc

    cmd_class = {"build_sphinx": BuildDoc}

if find_packages is not None:
    packages = find_packages()
else:
    packages = [
        "pyreadline",
        "pyreadline.clipboard",
        "pyreadline.configuration",
        "pyreadline.console",
        "pyreadline.keysyms",
        "pyreadline.lineeditor",
        "pyreadline.modes",
        "pyreadline.test",
    ]

# TODO: put this in an intermediate variable. append as needed
# for distutils setuptools compatabilit.
# TODO: add zip_safe=False

# Metadata: {{{
# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = "pyreadline"

# For versions with substrings (like 0.6.16.svn), use an extra . to separate
# the new substring.  We have to avoid using either dashes or underscores,
# because bdist_rpm does not accept dashes (an RPM) convention, and
# bdist_deb does not accept underscores (a Debian convention).
branch = ""

version = "2.0"

description = "A python implmementation of GNU readline."

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(ROOT_PATH, "", "README.rst")

with codecs.open(README, encoding="utf-8") as f:
    long_description = "\n" + f.read()


keywords = ["readline", "windows", "pyreadline"]
platforms = ["Windows XP/2000/NT", "Windows 95/98/ME", "Windows 10"]
url = "https://github.com/pyreadline/pyreadline"
download_url = "https://pypi.python.org/pypi/pyreadline"

license = "BSD"

authors = {
    "Jorgen": ("Jorgen Stenarson", "jorgen.stenarson@kroywen.se"),
    "Gary": ("Gary Bishop", ""),
    "Jack": ("Jack Trainor", ""),
}


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors["Jorgen"][0],
    author_email=authors["Jorgen"][1],
    maintainer=authors["Jorgen"][0],
    maintainer_email=authors["Jorgen"][1],
    license=license,
    # where did we define classifiers?
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    url=url,
    # check that this exists in setuptools
    download_url=download_url,
    platforms=platforms,
    keywords=keywords,
    # pretty sure you shouldn't do both modules and package
    # py_modules=["readline"],
    packages=packages,
    package_data={"pyreadline": ["configuration/*"]},
    data_files=[("doc", glob.glob("doc/*")),],
    cmdclass=cmd_class,
    python_requires=">=2.6.0",
    requires=["setuptools", "pywin32"],
    # They actually really don't but hey
    tests_require=["pytest"],
    extras_require={"docs": ["sphinx"]},
)
