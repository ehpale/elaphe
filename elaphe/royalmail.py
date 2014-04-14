# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class RoyalMail(Barcode):
    """
    >>> bc = RoyalMail()
    >>> bc # doctest: +ELLIPSIS
    <....RoyalMail object at ...>
    >>> print(bc.render_ps_code('LE28HS9Z')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 127 12
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <4c4532384853395a>
    <>
    /royalmail /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('LE28HS9Z', options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'royalmail'
    aliases = ('royal mail', 'royal-mail', 'royal_mail', 'rm4scc')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            includetext=False, includecheckintext=False,
            textsize=10, textyoffset=-7, height=0.175)

        def _code_bbox(self, codestring):
            """
            >>> r = RoyalMail._Renderer({})
            >>> r._code_bbox('LE28HS9Z')
            [0, 0, 127.296, 12.6]
            """
            height = self.lookup_option('height')
            codelen = len(codestring)*4+6
            return [0, 0, 1.44+codelen*(1.44+1.872), height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = RoyalMail._Renderer({})
            >>> r._text_bbox('LE28HS9Z')
            [0, 0, 127.296, 12.6]
            """
            if self.lookup_option('includetext'):
                textyoffset = self.lookup_option('textyoffset')
                textsize = self.lookup_option('textsize')
                cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
                return [cminx, cminy-textsize, cmaxx, cmaxy]
            else:
                return self._code_bbox(codestring)

        def build_params(self, codestring):
            params = super(RoyalMail._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
