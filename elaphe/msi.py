# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class MsiModifiedPlessey(Barcode):
    """
    >>> bc = MsiModifiedPlessey()
    >>> bc # doctest: +ELLIPSIS
    <....MsiModifiedPlessey object at ...>
    >>> print bc.render_ps_code('0123456789') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 169 72
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
    >>> bc.render('0123456789', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'msi'
    aliases = ('msi-plessey', 'msi plessey', 'msi_plessey', 'msiplessey')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=1,
            includecheck=False, includecheckintext=False, includetext=False,
            textyoffset=-7, textsize=10)

        def _code_bbox(self, codestring):
            """
            >>> r = MsiModifiedPlessey._Renderer({})
            >>> r._code_bbox('A0123456789B')
            [0, 0, 201, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, 4+(len(codestring)+1)*16+5, height*DPI]
            else:
                return [0, 0, 4+(len(codestring))*16+5, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = MsiModifiedPlessey._Renderer({})
            >>> r._text_bbox('A0123456789B')
            [0, -7, 201, 3]
            """
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]
        
        def build_params(self, codestring):
            params = super(MsiModifiedPlessey._Renderer, self).build_params(codestring)
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
