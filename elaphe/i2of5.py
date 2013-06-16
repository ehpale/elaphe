# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class Interleaved2of5(Barcode):
    """
    >>> bc = Interleaved2of5()
    >>> bc # doctest: +ELLIPSIS
    <....Interleaved2of5 object at ...>
    >>> print bc.render_ps_code('24012345678905') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -7 136 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (24012345678905) () interleaved2of5 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('24012345678905', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'interleaved2of5'
    aliases = ('interleaved_2_of_5', 'interleaved 2of5', 'interleaved_2of5',
               'interleaved 2 of 5', 'interleaved-2of5', 'i2of5', 'i-2of5')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            includecheck=False, includetext=False, textsize=10, textyoffset=-7, height=1)

        def _code_bbox(self, codestring):
            """
            >>> r = Interleaved2of5._Renderer({})
            >>> r._code_bbox('THIS IS CODE39')
            [0, 0, 136, 72.0]
            """
            height = self.lookup_option('height')
            return [0, 0, len(codestring)*9+4+6, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Interleaved2of5._Renderer({})
            >>> r._text_bbox('THIS IS CODE39')
            [0, -7, 136.0, 3]
            """
            hidestars = self.lookup_option('hidestars', False)
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            textmaxy = textyoffset + textsize
            textmaxx = 9*len(codestring)+4+0.6*textsize
            return [0, textyoffset, textmaxx, textmaxy]
        
        def build_params(self, codestring):
            params = super(Interleaved2of5._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
