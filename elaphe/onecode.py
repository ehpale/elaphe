# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class OneCode(Barcode):
    """
    >>> bc = OneCode()
    >>> bc # doctest: +ELLIPSIS
    <__main__.OneCode object at ...>
    >>> print bc.render_ps_code('0123456709498765432101234567891') # doctest: +ELLIPSIS
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
    (0123456709498765432101234567891) () onecode barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456709498765432101234567891', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    codetype = 'onecode'
    aliases = ()
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):

        @property
        def code_bbox(self):
            return [0, 0, 64*(1.44+1.872)+1.44, self.lookup_option('height', 0.175)]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-10, textyoffset-textsize/2.0, (12-1)*7+8+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
