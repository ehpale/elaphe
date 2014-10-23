# coding: utf-8
from __future__ import print_function
import re
from .base import Barcode, LinearCodeRenderer, DPI


CODE128_ESCAPE_RE = re.compile(r'\^\d{3}')
CODE128_CHARS =" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
class Code128(Barcode):
    """
    >>> bc = Code128()
    >>> bc # doctest: +ELLIPSIS
    <....Code128 object at ...>
    >>>
    >>> print(bc.render_ps_code('Count0123456789!', options=dict(includetext=True))) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -7 182 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <436f756e743031323334353637383921>
    <696e636c75646574657874>
    /code128 /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('Count0123456789!', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'code128'
    aliases = ('code_128', 'code-128', 'code 128')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1, includetext=False, 
            textyoffset=-7, textsize=10)

        def _count_chars(self, codestring):
            """
            >>> r = Code128._Renderer({})
            >>> r._count_chars('^104^102Count^0990123456789^101!')
            15
            """
            mode = -1
            idx = 0
            count = 0
            while idx<len(codestring):
                if codestring[idx] == '^':
                    code_i = int(codestring[idx+1:idx+4])
                    idx += 4
                else:
                    if mode==2:
                        code_i = int(codestring[idx:idx+2])
                        idx += 2
                    else:
                        code_i = CODE128_CHARS.find(codestring[idx])
                        idx += 1
                if code_i in (101, 103):
                    mode = 0
                elif code_i in (100, 104):
                    mode = 1
                elif code_i in (99, 105):
                    mode = 2
                count+=1
            return count
            
        def _code_bbox(self, codestring):
            """
            >>> r = Code128._Renderer({})
            >>> r._code_bbox('^104^102Count^0990123456789^101!')
            [0, 0, 167, 72.0]
            """
            height = self.lookup_option('height')
            return [0, 0, self._count_chars(codestring)*11+2, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code128._Renderer({})
            >>> r._text_bbox('^104^102Count^0990123456789^101!')
            [0, -7, 171.0, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            textmaxy = textyoffset + textsize
            textmaxx = 11*self._count_chars(codestring)+0.6*textsize
            return [0, textyoffset, textmaxx, textmaxy]
        
        def build_params(self, codestring):
            params = super(Code128._Renderer, self).build_params(codestring)
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
