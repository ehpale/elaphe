# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class UpcA(Barcode):
    """
    >>> bc = UpcA()
    >>> bc # doctest: +ELLIPSIS
    <__main__.UpcA object at ...>
    >>> print bc.render_ps_code('78858101497') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 88 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (78858101497) () upca barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('78858101497', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'upca'
    aliases = ('upc_a', 'upc-a', 'upc a')
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 12*7+4, DPI]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-7, textyoffset-textsize/2.0, 96+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


class UpcE(Barcode):
    """
    >>> bc = UpcE()
    >>> bc # doctest: +ELLIPSIS
    <__main__.UpcE object at ...>
    >>> print bc.render_ps_code('0123456') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 39 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (0123456) () upce barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'upce'
    aliases = ('upc_e', 'upc-e', 'upc e')
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 5*7+4, DPI]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-7, textyoffset-textsize/2.0, 6*7+11+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
