# coding: utf-8
from __future__ import print_function
import re
from .base import Barcode, LinearCodeRenderer, DPI


CODE39_ESCAPE_RE = re.compile(r'\^\d{3}')
CODE39_CHARS ="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%*"
class Code39(Barcode):
    """
    >>> bc = Code39()
    >>> bc # doctest: +ELLIPSIS
    <....Code39 object at ...>
    >>>
    >>> print(bc.render_ps_code('CODE39')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 128 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <434f44453339>
    <>
    /code39 /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('CODE39', options=dict(includecheck=True, includetext=True, includecheckintext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'code39'
    aliases = ('code_39', 'code-39', 'code 39')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1, hidestars=False,
            includecheck=False, includetext=False,
            includecheckintext=False,
            textyoffset=-7, textsize=10)

        def _codelen(self, codestring):
            if self.lookup_option('includecheck', False)==True:
                codelen = len(codestring)+3
            else:
                codelen = len(codestring)+2
            return codelen
            
        def _code_bbox(self, codestring):
            """
            >>> r = Code39._Renderer({})
            >>> r._code_bbox('THIS IS CODE39')
            [0, 0, 256, 72.0]
            """
            height = self.lookup_option('height')
            return [0, 0, self._codelen(codestring)*16, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code39._Renderer({})
            >>> r._text_bbox('THIS IS CODE39')
            [0, -7, 246.0, 3]
            """
            hidestars = self.lookup_option('hidestars')
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            textmaxy = textyoffset + textsize
            textminx = 0
            textmaxx = 16*(len(codestring)+1)+0.6*textsize
            if hidestars:
                textminx, textmaxx = 16, textmaxx-16
            return [0, textyoffset, textmaxx, textmaxy]
        
        def build_params(self, codestring):
            params = super(Code39._Renderer, self).build_params(codestring)
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
