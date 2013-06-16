# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class Code2of5(Barcode):
    """
    >>> bc = Code2of5()
    >>> bc # doctest: +ELLIPSIS
    <....Code2of5 object at ...>
    >>> print bc.render_ps_code('0123456789') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 160 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (0123456789) () code2of5 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456789', options=dict(includetext=False, includecheck=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'code2of5'
    aliases = ('code_2_of_5', 'code 2of5', 'code_2of5',
               'code 2 of 5', 'code-2of5', 'c2of5', 'c-2of5',
               'code25', 'code 25', 'code_25', 'code-25')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1,
            includecheck=False, includetext=False,
            includecheckintext=False,
            textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = Code2of5._Renderer({})
            >>> r._code_bbox('0123456789')
            [0, 0, 160, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, 6+(len(codestring)+1)*14+14, height*DPI]
            else:
                return [0, 0, 6+len(codestring)*14+14, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code2of5._Renderer({})
            >>> r._text_bbox('0123456789')
            [0, -7, 160, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(Code2of5._Renderer, self).build_params(codestring)
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
