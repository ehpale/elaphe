# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class Plessey(Barcode):
    """
    >>> bc = Plessey()
    >>> bc # doctest: +ELLIPSIS
    <....Plessey object at ...>
    >>> print(bc.render_ps_code('01234ABCD')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 265 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <303132333441424344>
    <>
    /plessey /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('01234ABCD', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('01234ABCD', options=dict(includetext=True, includecheckintext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('01234ABCD', options=dict(unidirectional=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'plessey'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            dontdraw=False, includetext=False, validatecheck=False,
            includecheckintext=False, unidirectional=False,
            textsize=10, textyoffset=-7, height=1)

        def _code_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._code_bbox('A012345ABCDB')
            [0, 0, 325, 72.0]
            """
            height = self.lookup_option('height')
            includecheck = self.lookup_option('includecheck')
            unidirectional = self.lookup_option('unidirectional')
            endchar = 8 if unidirectional else 25
            return [0, 0, 20+(len(codestring)+2)*20+endchar, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Plessey._Renderer({})
            >>> r._text_bbox('A012345ABCDB')
            [0, -7, 325, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(Plessey._Renderer, self).build_params(codestring)
            text_bbox = (self._text_bbox(codestring) if self.lookup_option('includetext')==True
                         else [0, 0, 0, 0])
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), text_bbox)
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
