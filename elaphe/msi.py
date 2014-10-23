# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class MsiModifiedPlessey(Barcode):
    """
    >>> bc = MsiModifiedPlessey()
    >>> bc # doctest: +ELLIPSIS
    <....MsiModifiedPlessey object at ...>
    >>> print(bc.render_ps_code('0123456789')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 127 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <30313233343536373839>
    <>
    /msi /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456789', options=dict(includecheck=True, includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
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
            [0, 0, 151, 72.0]
            """
            height = self.lookup_option('height')
            if self.lookup_option('includecheck'):
                return [0, 0, 3+(len(codestring)+2)*12+4, height*DPI]
            else:
                return [0, 0, 3+(len(codestring))*12+4, height*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = MsiModifiedPlessey._Renderer({})
            >>> r._text_bbox('A0123456789B')
            [0, -7, 151, 3]
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
