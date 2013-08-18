# coding: utf-8

from bases import Barcode

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
        except ImportError, e:
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
    """
    # search for codetype registry
    renderer = Barcode.resolve_codetype(codetype)
    if renderer:
        return renderer().render(codestring, options=options, **kw)
    raise ValueError(u'No renderer for codetype %s' %codetype)


if __name__=="__main__":
    from doctest import testmod
    testmod()

"""elaphe -- A Python binding for Barcode Writer In Pure Postscrpt.
"""
__version__=(0, 5, 6)
