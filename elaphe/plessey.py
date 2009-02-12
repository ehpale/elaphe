# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Plessey(Barcode):
    """
    >>> bc = Plessey()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Plessey object at ...>
    >>> print bc.render_ps_code('012345ABCD') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 227 72
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
    >>> bc.render('012345ABCD', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'plessey'
    aliases = ('rationalized codabar')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._code_bbox('A012345ABCDB')
            [0, 0, 259, 72.0]
            """
            if self.lookup_option('includecheck', False)==None:
                return [0, 0, (len(codestring)+1)*16+48+19, DPI]
            else:
                return [0, 0, (len(codestring))*16+48+19, DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._text_bbox('A012345ABCDB')
            [0, -5.0, 259, 72.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]
        
        def build_params(self, codestring):
            params = super(Plessey._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
