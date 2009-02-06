# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Ean13(Barcode):
    """
    >>> bc = Ean13()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean13 object at ...>
    >>> print bc.render_ps_code('977147396801') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 95 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (977147396801) () ean13 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('977147396801', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    codetype = 'ean13'
    aliases = ('ean_13', 'ean-13', 'ean 13', 'jan')
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 13*7+4, DPI]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-10, textyoffset-textsize/2.0, (12-1)*7+8+textsize, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
