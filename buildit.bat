python setup.py build

python setup.py bdist_wheel
:: python setup.py bdist_wininst --plat-name=win32
:: python setup.py bdist_wininst --plat-name=win-amd64
python setup.py sdist
python setup.py build_sphinx
