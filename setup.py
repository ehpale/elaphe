# -*- coding: utf-8 -*-
import sys, os
from os.path import abspath, dirname, join as pathjoin
from setuptools import setup

sys.path.insert(0, abspath('./tests'))
sys.path.insert(0, abspath('./elaphe'))

import elaphe

version = '.'.join(map(str, elaphe.__version__))

install_requires = ['setuptools', 'PIL']
test_requires = []
extra_requires = {}
long_description = '\n'.join([
    open(pathjoin(dirname(abspath(__file__)), 'README')).read(),
    open(pathjoin(dirname(abspath(__file__)), 'LICENSE')).read(),
    ])

setup_params = dict(
    name="elaphe",
    version=version,
    packages=['elaphe'],
    exclude_package_data={'elaphe': ['postscriptbarcode']},
    package_data={'elaphe': ['postscriptbarcode/barcode.ps', 'postscriptbarcode/LICENSE']},
    zip_safe=False,
    dependency_links = ["http://dist.repoze.org"], #PIL as egg
    install_requires = install_requires,
    tests_require=test_requires,
    extras_require=extra_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author = "Yasushi Masuda",
    author_email = "whosaysni at gmail dot com",
    description = "Generates various barcodes using barcode.ps and PIL.",
    long_description=long_description,
    license = "New BSD",
    keywords = "barcode convert postscript image graphics",
    url = "http://elaphe.googlecode.com",
    download_url = "http://code.google.com/p/elaphe/downloads/list",
    # entry_points = {'console_scripts': ['elaphe = elaphe.:main']},
    test_suite = 'runner',
)

setup(**setup_params)
