# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class RoyalMail(Barcode):
    """
    >>> bc = RoyalMail()
    >>> bc # doctest: +ELLIPSIS
    <__main__.RoyalMail object at ...>
    >>> print bc.render_ps_code('LE28HS9Z') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 127 9
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (LE28HS9Z) () royalmail barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('LE28HS9Z', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'royalmail'
    aliases = ('royal mail', 'royal-mail', 'royal_mail', 'rm4scc')
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):

        def _code_bbox(self, codestring):
            """
            >>> r = RoyalMail._Renderer({})
            >>> r._code_bbox('LE28HS9Z')
            [0, 0, 127.29600000000001, 9.0]
            """
            codelen = len(codestring)*4+6
            return [0, 0, codelen*(1.44+1.872)+1.44, self.lookup_option('height', 0.125)*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = RoyalMail._Renderer({})
            >>> r._text_bbox('LE28HS9Z')
            [0, -5.0, 127.29600000000001, 9.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]

        def build_params(self, codestring):
            params = super(RoyalMail._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
