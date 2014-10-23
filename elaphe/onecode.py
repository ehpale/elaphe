# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI

class OneCode(Barcode):
    """
    >>> bc = OneCode()
    >>> bc # doctest: +ELLIPSIS
    <....OneCode object at ...>
    >>> print(bc.render_ps_code('0123456709498765432101234567891')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 213 12
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <30313233343536373039343938373635343332313031323334353637383931>
    <>
    /onecode /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('0123456709498765432101234567891', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'onecode'
    aliases = ('usps onecode', 'uspsonecode', 'usps-onecode', 'usps_onecode')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=0.175, textyoffset=-9, textsize=12)

        @property
        def code_bbox(self):
            height = self.lookup_option('height')
            return [0, 0, 64*(1.44+1.872)+1.44, height*DPI]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset')
            textsize = self.lookup_option('textsize')
            if self.lookup_option('includetext'):
                return [0, textyoffset, (12-1)*7+8+textsize*0.6, textyoffset+textsize]
            else:
                return self.code_bbox
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
