# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class Kix(Barcode):
    """
    >>> bc = Kix()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Kix object at ...>
    >>> print bc.render_ps_code('1231FZ13XHS') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 147 9
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (1231FZ13XHS) () kix barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('1231FZ13XHS', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'kix'
    aliases = ()
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):

        def _code_bbox(self, codestring):
            """
            >>> r = Kix._Renderer({})
            >>> r._code_bbox('5956439111ABA 9')
            [0, 0, 200.16000000000003, 9.0]
            """
            return [0, 0, 4*len(codestring)*(1.44+1.872)+1.44,
                    self.lookup_option('height', 0.125)*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Kix._Renderer({})
            >>> r._text_bbox('LE28HS9Z')
            [0, -5.0, 107.42400000000001, 9.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]

        def build_params(self, codestring):
            params = super(Kix._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
