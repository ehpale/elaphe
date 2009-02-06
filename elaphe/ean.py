# coding: utf-8
from bases import BarcodeRenderer, LinearBarcode

class Ean13(BarcodeRenderer, LinearBarcode):
    """
    >>> bc = Ean13()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean13 object at ...>
    >>> print bc.render_ps_code('977147396801') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: -20 -20 164 92
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    (977147396801) () ean13 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('977147396801') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    codetype = 'ean13'
    aliases = ('ean_13', 'jan')
    default_options = {}


if __name__=="__main__":
    from doctest import testmod
    testmod()
