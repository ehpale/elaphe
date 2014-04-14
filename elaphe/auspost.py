# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI


class AusPost(Barcode):
    """
    >>> bc = AusPost()
    >>> bc # doctest: +ELLIPSIS
    <....AusPost object at ...>
    >>> print(bc.render_ps_code('6279438541AaaB 155')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 223 12
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <363237393433383534314161614220313535>
    <>
    /auspost /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('6279438541AaaB 155', options=dict(includetext=False), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('6279438541AaaB 155', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('593221132401234567', options=dict(includetext=True, custinfoenc='numeric'), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'auspost'
    aliases = ()

    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=0.175,
            includetext=False, textyoffset=-7, textsize=10,
            custinfoenc='character')
        def _code_length(self, codestring):
            head = codestring[:2]
            if head in ['11', '45']:
                codelen = 37
            elif head in ['59']:
                codelen = 52
            elif head in ['62']:
                codelen = 67
            else:
                raise ValueError('Invalid code header.')
            return codelen
        
        def _code_bbox(self, codestring):
            """
            >>> r = AusPost._Renderer({})
            >>> r._code_bbox('5956439111ABA 9')
            [0, 0, 173.66400000000002, 12.6]
            """
            return [0, 0, self._code_length(codestring)*(1.44+1.872)+1.44,
                    self.lookup_option('height')*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = AusPost._Renderer({})
            >>> r._text_bbox('5956439111ABA 9')
            [0, -7, 173.66400000000002, 3]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, textyoffset, cmaxx, textyoffset+textsize]

        def build_params(self, codestring):
            params = super(AusPost._Renderer, self).build_params(codestring)
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
