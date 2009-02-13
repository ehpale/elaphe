# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Raw(Barcode):
    """
    >>> bc = Raw()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Raw object at ...>
    >>> print bc.render_ps_code('331132131313411122131311333213114131131221323') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 90 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (331132131313411122131311333213114131131221323) () raw barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('331132131313411122131311333213114131131221323', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'raw'
    aliases = ()
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = Raw._Renderer({})
            >>> r._code_bbox('331132131313411122131311333213114131131221323')
            [0, 0, 90, 72.0]
            """
            return [0, 0, sum(int(c) for c in list(codestring)), DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Raw._Renderer({})
            >>> r._text_bbox('331132131313411122131311333213114131131221323')
            [0, -5.0, 90, 72.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]
        
        def build_params(self, codestring):
            params = super(Raw._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
