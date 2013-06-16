# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Plessey(Barcode):
    """
    >>> bc = Plessey()
    >>> bc # doctest: +ELLIPSIS
    <....Plessey object at ...>
    >>> print bc.render_ps_code('012345ABCD') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -7 227 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (012345ABCD) () plessey barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('012345ABCD', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'plessey'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            includetext=False, includecheckintext=False,
            textsize=10, textyoffset=-7, height=1)

        def _code_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._code_bbox('A012345ABCDB')
            [0, 0, 259, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, (len(codestring)+1)*16+48+19, height*DPI]
            else:
                return [0, 0, (len(codestring))*16+48+19, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._text_bbox('A012345ABCDB')
            [0, -7, 259, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(Plessey._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
