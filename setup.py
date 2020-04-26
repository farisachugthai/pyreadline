# -*- coding: utf-8 -*-

# *****************************************************************************
#       Copyright (C) 2003-2006 Gary Bishop.
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

import os
import sys
import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    find_packages = None
else:
    from setuptools import find_packages

from platform import system

# This doesn't do anything because linux can pip install it
# _S = system()
# if "windows" != _S.lower():
#     raise RuntimeError("pyreadline is for Windows only, not {}.".format(_S))

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists("MANIFEST"):
    os.remove("MANIFEST")
#

exec(compile(open("pyreadline/release.py").read(), "pyreadline/release.py", "exec"))

try:
    import sphinx
    from sphinx.setup_command import BuildDoc

    cmd_class = {"build_sphinx": BuildDoc}
except ImportError:
    cmd_class = {}

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
    classifiers=classifiers,
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
)
