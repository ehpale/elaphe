# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class MsiModifiedPlessey(Barcode):
    """
    >>> bc = MsiModifiedPlessey()
    >>> bc # doctest: +ELLIPSIS
    <__main__.MsiModifiedPlessey object at ...>
    >>> print bc.render_ps_code('0123456789') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 169 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (0123456789) () msi barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456789', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'msi'
    aliases = ('msi-plessey', 'msi plessey', 'msi_plessey', 'msiplessey')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = MsiModifiedPlessey._Renderer({})
            >>> r._code_bbox('A0123456789B')
            [0, 0, 201, 72.0]
            """
            if self.lookup_option('includecheck', False)==None:
                return [0, 0, 4+(len(codestring)+1)*16+5, DPI]
            else:
                return [0, 0, 4+(len(codestring))*16+5, DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = MsiModifiedPlessey._Renderer({})
            >>> r._text_bbox('A0123456789B')
            [0, -5.0, 201, 72.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]
        
        def build_params(self, codestring):
            params = super(MsiModifiedPlessey._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
