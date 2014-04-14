# coding: utf-8
"""elaphe -- A Python binding for Barcode Writer In Pure Postscrpt.
"""
from .base import Barcode
from .__version__ import VERSION

DEFAULT_PLUGINS = [
    'elaphe.ean', 'elaphe.upc', 'elaphe.code128', 'elaphe.code39',
    'elaphe.code93', 'elaphe.i2of5', 'elaphe.rss', 'elaphe.pharmacode',
    'elaphe.code25', 'elaphe.code11', 'elaphe.codabar', 'elaphe.onecode',
    'elaphe.postnet', 'elaphe.royalmail', 'elaphe.auspost', 'elaphe.kix',
    'elaphe.japanpost', 'elaphe.msi', 'elaphe.plessey', 'elaphe.raw',
    'elaphe.symbol', 'elaphe.pdf417', 'elaphe.datamatrix', 'elaphe.qrcode',
    'elaphe.maxicode', 'elaphe.azteccode']

if __name__=="__main__":
    DEFAULT_PLUGINS = [s.replace('elaphe.', '') for s in DEFAULT_PLUGINS]
    

def load_plugins():
    for PL in DEFAULT_PLUGINS:
        try:
            __import__(PL, fromlist=[PL])
        except ImportError as e:
            import sys
            sys.stdout.write(u'Warning: %s\n' %e)
    Barcode.update_codetype_registry()
load_plugins()


def barcode(codetype, codestring, options=None, **kw):
    """

    >>> barcode('nonexistent', '977147396801')
    Traceback (most recent call last):
    ...
    ValueError: No renderer for codetype nonexistent
    >>> barcode('qrcode', 'Hello Barcode Writer In Pure PostScript.', 
    ...         options=dict(version=9, eclevel='M'), margin=10, data_mode='8bits') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('code128', '^104^102Count^0990123456789^101!', 
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('pdf417', '^453^178^121^239', 
    ...         options=dict(columns=2, rows=10), margin=1, scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('upca', '78858101497', 
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> barcode('upce', '0123456', 
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('royalmail', 'LE28HS9Z', 
    ...         options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('datamatrix', '^142^164^186', 
    ...         options=dict(columns=32, rows=32), margin=1, scale=2.0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('code11', '0123456789', 
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('code25', '0123456789', 
    ...         options=dict(includetext=False, includecheck=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('code39', 'THIS IS CODE39',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('code93', 'THIS IS CODE93',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('japanpost', '1231FZ13XHS',
    ...         options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('azteccode', '00100111001000000101001101111000010100111100101000000110',
    ...         margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('auspost', '5956439111ABA 9',
    ...         options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('ean13', '977147396801',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('interleaved2of5', '24012345678905',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('raw', '331132131313411122131311333213114131131221323',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('kix', '1231FZ13XHS',
    ...         options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('postnet', '012345',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('pharmacode', '117480',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('plessey', '012345ABCD',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('symbol', 'fimd',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('onecode', '0123456709498765432101234567891',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('maxicode', '^059^042^041^059^040^03001^02996152382802^029840^029001^0291Z00004951^029UPSN^02906X610^029159^0291234567^0291^0471^029^029Y^029634 ALPHA DR^029PITTSBURGH^029PA^030^062^004^063',
    ...         options=dict(mode=2), margin=1, scale=4) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('msi', '0123456789',
    ...         options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('rss14', '24012345678905',
    ...         options=dict(linkage=True, includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    >>> barcode('rationalizedCodabar', 'A0123456789B',
    ...         options=dict(includetext=True, includecheck=True), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ...>
    >>> # _.show()
    """
    # search for codetype registry
    renderer = Barcode.resolve_codetype(codetype)
    if renderer:
        return renderer().render(codestring, options=options, **kw)
    raise ValueError(u'No renderer for codetype %s' %codetype)


if __name__=="__main__":
    from doctest import testmod
    testmod()
