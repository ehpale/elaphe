# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class PostNet(Barcode):
    """
    >>> bc = PostNet()
    >>> bc # doctest: +ELLIPSIS
    <__main__.PostNet object at ...>
    >>> print bc.render_ps_code('012345') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 123 9
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (012345) () postnet barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('012345', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'postnet'
    aliases = ()
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):

        def _code_bbox(self, codestring):
            """
            >>> r = PostNet._Renderer({})
            >>> r._code_bbox('0123456789')
            [0, 0, 190.22400000000002, 9.0]
            """
            codelen = 7+len(codestring)*5
            return [0, 0, codelen*(1.44+1.872)+1.44, 0.125*DPI] # self.lookup_option('height', 0.125)*5]

        def _text_bbox(self, codestring):
            """
            >>> r = PostNet._Renderer({})
            >>> r._text_bbox('0123456789')
            [0, -5.0, 190.22400000000002, 9.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]

        def build_params(self, codestring):
            params = super(PostNet._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
