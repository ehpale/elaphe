# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class PostNet(Barcode):
    """
    >>> bc = PostNet()
    >>> bc # doctest: +ELLIPSIS
    <....PostNet object at ...>
    >>> print(bc.render_ps_code('12345123412')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 203 9
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <3132333435313233343132>
    <>
    /postnet /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('12345123412', options=dict(includecheckintext=True, includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'postnet'
    aliases = ('post net', 'post-net', 'post_net', 'us-postnet', 'us postnet', 'us_postnet')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            includetext=False, includecheckintext=False,
            textsize=10, textyoffset=-7, height=0.125)

        def _code_bbox(self, codestring):
            """
            >>> r = PostNet._Renderer({})
            >>> r._code_bbox('0123456789')
            [0, 0, 186.912, 9.0]
            """
            height = self.lookup_option('height')
            codelen = 7+len(codestring)*5
            return [0, 0, codelen*(1.44+1.872)-1.872, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = PostNet._Renderer({})
            >>> r._text_bbox('0123456789')
            [0, -7, 186.912, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]

        def build_params(self, codestring):
            params = super(PostNet._Renderer, self).build_params(codestring)
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
