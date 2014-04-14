# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class Raw(Barcode):
    """
    >>> bc = Raw()
    >>> bc # doctest: +ELLIPSIS
    <....Raw object at ...>
    >>> print(bc.render_ps_code('331132131313411122131311333213114131131221323')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 90 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <33333131333231333133313334313131323231333133313133333332313331313431333
     1313331323231333233>
    <>
    /raw /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('331132131313411122131311333213114131131221323', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'raw'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            textyoffset=-7, textsize=10, height=1)

        def _code_bbox(self, codestring):
            """
            >>> r = Raw._Renderer({})
            >>> r._code_bbox('331132131313411122131311333213114131131221323')
            [0, 0, 90, 72.0]
            """
            height = self.lookup_option('height')
            return [0, 0, sum(int(c) for c in list(codestring)), height*DPI]

        def build_params(self, codestring):
            params = super(Raw._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._code_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
