# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class RationalizedCodabar(Barcode):
    """
    >>> bc = RationalizedCodabar()
    >>> bc # doctest: +ELLIPSIS
    <....RationalizedCodabar object at ...>
    >>> print bc.render_ps_code('A0123456789B') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 148 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (A0123456789B) () rationalizedCodabar barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('A0123456789B', options=dict(includetext=None, includecheck=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'rationalizedCodabar'
    aliases = ('rationalized codabar')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1,
            includecheck=False, includetext=False,
            includecheckintext=False,
            textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = RationalizedCodabar._Renderer({})
            >>> r._code_bbox('A0123456789B')
            [0, 0, 148, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, 14+(len(codestring)-2)*12+14+14, height*DPI]
            else:
                return [0, 0, 14+(len(codestring)-2)*12+14, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = RationalizedCodabar._Renderer({})
            >>> r._text_bbox('A0123456789B')
            [0, -7, 148, 3]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(RationalizedCodabar._Renderer, self).build_params(codestring)
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
