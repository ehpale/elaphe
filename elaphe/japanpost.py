# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI


class JapanPost(Barcode):
    """
    >>> bc = JapanPost()
    >>> bc # doctest: +ELLIPSIS
    <....JapanPost object at ...>
    >>> print(bc.render_ps_code('1231FZ13XHS')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 220 12
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <31323331465a3133584853>
    <>
    /japanpost /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('1231FZ13XHS', options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'japanpost'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=0.175, includetext=False, includecheckintext=False,
            textyoffset=-7, textsize=10)

        @property
        def code_bbox(self):
            height = self.lookup_option('height')
            return [0, 0, (21*3+3)*(1.44+1.872)+1.44, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = JapanPost._Renderer({})
            >>> r._text_bbox('LE28HS9Z')
            [0, -7, 220.032, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self.code_bbox
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]

        def build_params(self, codestring):
            params = super(JapanPost._Renderer, self).build_params(codestring)
            cbbox = self.code_bbox
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
