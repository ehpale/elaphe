# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Symbol(Barcode):
    """
    >>> bc = Symbol()
    >>> bc # doctest: +ELLIPSIS
    <....Symbol object at ...>
    >>> print bc.render_ps_code('fima') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 38 45
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (fima) () symbol barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('fimd', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'symbol'
    aliases = ('symbols', 'fimsymbols', 'fim symbols', 'fim-symbols', 'fim_symbols')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(LinearCodeRenderer.default_options)
        _widths = dict(
            fima=sum([2.25, 2.25, 2.25, 11.25, 2.25, 11.25, 2.25, 2.25, 2.25]),
            fimb=sum([2.25, 6.75, 2.25, 2.25, 2.25, 6.25, 2.25, 2.25, 2.25, 6.75, 2.25]),
            fimc=sum([2.25, 2.25, 2.25, 6.75, 2.25, 6.75, 2.25, 6.75, 2.25, 2.25, 2.25]),
            fimd=sum([2.25, 2.25, 2.25, 2.25, 2.25, 6.75, 2.25, 6.75, 2.25, 2.25, 2.25, 2.25, 2.25]))

        def _code_bbox(self, codestring):
            """
            >>> r = Symbol._Renderer({})
            >>> r._code_bbox('fima')
            [0, 0, 38.25, 45.0]
            """
            return [0, 0, self._widths[codestring], 0.625*DPI]

        def build_params(self, codestring):
            params = super(Symbol._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._code_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()


