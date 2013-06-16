# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class Code11(Barcode):
    """
    >>> bc = Code11()
    >>> bc # doctest: +ELLIPSIS
    <....Code11 object at ...>
    >>> print bc.render_ps_code('0123456789') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 110 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (0123456789) () code11 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456789', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'code11'
    aliases = ('code 11', 'code_11', 'code-11')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1,
            includecheck=False, includetext=False,
            includecheckintext=False,
            textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = Code11._Renderer({})
            >>> r._code_bbox('0123456789')
            [0, 0, 110, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, 10+len(codestring)*10+10+10, height*DPI]
            else:
                return [0, 0, 10+len(codestring)*10, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Code11._Renderer({})
            >>> r._text_bbox('0123456789')
            [0, -7, 110, 3]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(Code11._Renderer, self).build_params(codestring)
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
