# -*- coding: utf-8 -*-
import io
import os

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8'),
    ) as fp:
        return fp.read()

readme = open('README.rst').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')


setup(
    name="elaphe3",
    version='0.1.2.dev0',
    packages=['elaphe'],
    exclude_package_data={
        'elaphe': ['postscriptbarcode']},
    package_data={
        'elaphe': ['postscriptbarcode/barcode.ps',
                   'postscriptbarcode/LICENSE']},
    zip_safe=False,
    install_requires=['pillow'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author="Yasushi Masuda",
    author_email="whosaysni@gmail.com",
    maintainer='Thomas Grainger',
    maintainer_email='elaphe3@graingert.co.uk',
    description="Generates various barcodes using barcode.ps and pillow.",
    long_description=readme + '\n\n' + history,
    license="New BSD",
    keywords="barcode convert postscript image graphics",
    url="https://github.com/graingert/elaphe",
    test_suite='test.suite',
)
