# coding: utf-8
from bases import Barcode

DEFAULT_PLUGINS = ('ean', 'upc', 'code128', 'code39', 'code93', 'i2of5', 'qrcode',)


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
    """
    # search for codetype registry
    renderer = Barcode.resolve_codetype(codetype)
    if renderer:
        return renderer().render(codestring, options=options, **kw)
    raise ValueError(u'No renderer for codetype %s' %codetype)


if __name__=="__main__":
    from doctest import testmod
    testmod()
