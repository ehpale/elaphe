# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class UpcA(Barcode):
    """
    >>> bc = UpcA()
    >>> bc # doctest: +ELLIPSIS
    <....UpcA object at ...>
    >>> print bc.render_ps_code('78858101497') # doctest: +ELLIPSIS
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
    (78858101497) () upca barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('78858101497', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'upca'
    aliases = ('upc_a', 'upc-a', 'upc a')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            includetext=False, textsize=12, textyoffset=-4, height=1)

        @property
        def code_bbox(self):
            height = self.lookup_option('height')
            return [0, 0, 3+12*7+3+5, DPI*height]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext'):
                return [-7, textyoffset, 96+textsize*0.5, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


class UpcE(Barcode):
    """
    >>> bc = UpcE()
    >>> bc # doctest: +ELLIPSIS
    <....UpcE object at ...>
    >>> print bc.render_ps_code('0123456') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 53 72
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
    >>> bc.render('0123456', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'upce'
    aliases = ('upc_e', 'upc-e', 'upc e')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            textsize=12, textyoffset=-4, height=1)

        @property
        def code_bbox(self):
            height = self.lookup_option('height')
            return [0, 0, 4+6*7+7, DPI*height]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext'):
                return [-7, textyoffset, 6*7+11+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
