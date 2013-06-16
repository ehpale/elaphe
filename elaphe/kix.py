# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class Kix(Barcode):
    """
    >>> bc = Kix()
    >>> bc # doctest: +ELLIPSIS
    <....Kix object at ...>
    >>> print bc.render_ps_code('1231FZ13XHS') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 147 12
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
    >>> bc.render('1231FZ13XHS', options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'kix'
    aliases = ('dutch kix', 'dutch-kix', 'dutch_kix')

    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=0.175, includetext=False, includecheckintext=False,
            textsize=10, textyoffset=-7)

        def _code_bbox(self, codestring):
            """
            >>> r = Kix._Renderer({})
            >>> r._code_bbox('5956439111ABA 9')
            [0, 0, 200.16000000000003, 12.6]
            """
            height = self.lookup_option('height')
            return [0, 0, 4*len(codestring)*(1.44+1.872)+1.44, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Kix._Renderer({})
            >>> r._text_bbox('LE28HS9Z')
            [0, -7, 107.424, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]

        def build_params(self, codestring):
            params = super(Kix._Renderer, self).build_params(codestring)
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
