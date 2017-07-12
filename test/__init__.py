from unittest import TestSuite
from doctest import DocTestSuite
from . import render

module_names = [
    'elaphe',
    'elaphe.util',
    'elaphe.base',
    'elaphe.auspost',
    'elaphe.azteccode',
    'elaphe.codabar',
    'elaphe.code11',
    'elaphe.code128',
    'elaphe.code25',
    'elaphe.code39',
    'elaphe.code93',
    'elaphe.datamatrix',
    'elaphe.ean',
    'elaphe.i2of5',
    'elaphe.japanpost',
    'elaphe.kix',
    'elaphe.maxicode',
    'elaphe.msi',
    'elaphe.onecode',
    'elaphe.pdf417',
    'elaphe.pharmacode',
    'elaphe.plessey',
    'elaphe.postnet',
    'elaphe.qrcode',
    'elaphe.raw',
    'elaphe.royalmail',
    'elaphe.rss',
    'elaphe.symbol',
    'elaphe.upc',
    ]

suite = TestSuite()

# doctests
for module_name in module_names:
    suite.addTest(DocTestSuite(module_name))


render.collect(suite)
