# coding: utf-8
import re
from bases import Barcode, LinearCodeRenderer, DPI


CODE128_ESCAPE_RE = re.compile(r'\^\d{3}')
CODE128_CHARS =" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
class Code128(Barcode):
    """
    >>> bc = Code128()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Code128 object at ...>
    >>>
    # >>> print bc.render_ps_code('^104^102Count^0990123456789^101!') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 136 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (^104^102Count^0990123456789^101!) () upca barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('^104^102Count^0990123456789^101!', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'code128'
    aliases = ('code_128', 'code-128', 'code 128')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10)
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
            [0, 0, 189, 72.0]
            """
            return [0, 0, self._count_chars(codestring)*11+11+13, DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code128._Renderer({})
            >>> r._text_bbox('^104^102Count^0990123456789^101!')
            [0, -12.0, 171.0, 3]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            textmaxy = textyoffset + textsize
            textmaxx = 11*self._count_chars(codestring)+0.6*textsize
            return [0, textyoffset-textsize/2.0, textmaxx, textmaxy]
        
        def build_params(self, codestring):
            params = super(Code128._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params

    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
