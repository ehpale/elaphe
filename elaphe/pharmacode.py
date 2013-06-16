# coding: utf-8
import re, math
from bases import Barcode, LinearCodeRenderer, DPI

class Phamacode(Barcode):
    """
    >>> bc = Phamacode()
    >>> bc # doctest: +ELLIPSIS
    <....Phamacode object at ...>
    >>>
    >>> print bc.render_ps_code('117480') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 90 22
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (117480) () pharmacode barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('117480', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'pharmacode'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=8*2.835, nwidth=0.5*2.835,
            wwidth=1.5*2.835, swidth=1.0*2.835,
            textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = Phamacode._Renderer({})
            >>> r._code_bbox('117480')
            [0, 0, 90.72, 22.68]
            """
            return [0, 0, int(math.log(int(codestring), 2))*2*2.835,
                    self.lookup_option('height')]

        def _text_bbox(self, codestring):
            """
            >>> r = Phamacode._Renderer({})
            >>> r._text_bbox('117480')
            [0, -7, 90.72, 3]
            """
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            textsize = self.lookup_option('textsize')
            textyoffset = self.lookup_option('textyoffset')
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(Phamacode._Renderer, self).build_params(codestring)
            cbbox = self._code_bbox(codestring)
            if self.lookup_option('includetext'):
                tbbox = self._text_bbox(codestring)
            else:
                tbbox = cbbox
            params['bbox'] = "%d %d %d %d" %self._boundingbox(cbbox, tbbox)
            return params

    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
