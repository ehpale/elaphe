# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI


class AusPost(Barcode):
    """
    >>> bc = AusPost()
    >>> bc # doctest: +ELLIPSIS
    <__main__.AusPost object at ...>
    >>> print bc.render_ps_code('5956439111ABA 9') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 173 9
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (5956439111ABA 9) () auspost barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('5956439111ABA 9', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'auspost'
    aliases = ()
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):

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
            [0, 0, 173.66400000000002, 9.0]
            """
            return [0, 0, self._code_length(codestring)*(1.44+1.872)+1.44,
                    self.lookup_option('height', 0.125)*DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = AusPost._Renderer({})
            >>> r._text_bbox('5956439111ABA 9')
            [0, -5.0, 173.66400000000002, 9.0]
            """
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
            return [cminx, cminy-textsize/2.0, cmaxx, cmaxy]

        def build_params(self, codestring):
            params = super(AusPost._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
