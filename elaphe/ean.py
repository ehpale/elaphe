# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Ean13(Barcode):
    """
    >>> bc = Ean13()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean13 object at ...>
    >>> print bc.render_ps_code('977147396801') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 95 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (977147396801) () ean13 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('977147396801', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> #_.show()
    """
    codetype = 'ean13'
    aliases = ('ean_13', 'ean-13', 'ean 13', 'jan')
    default_options = dict(textyoffset=-4)
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 13*7+4, DPI]

        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-10, textyoffset-textsize/2.0, (12-1)*7+8+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


class ISBN(Ean13):
    """
    >>> bc = ISBN()
    >>> bc # doctest: +ELLIPSIS
    <__main__.ISBN object at ...>
    >>> print bc.render_ps_code('978-1-56592-479') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 95 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (978-1-56592-479) () isbn barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('978-1-56592-479', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> #_.show()
    """
    codetype = 'isbn'
    aliases = ()
    class _Renderer(Ean13._Renderer):
        def build_codestring(self, codestring):
            """
            Allows to accept digit-only notation.
            >>> ISBN._Renderer({}).build_codestring('978 1 56592 479')
            '(978-1-56592-479)'
            """
            cs = "%s%s%s-%s-%s%s%s%s%s-%s%s%s" %tuple(c for c in  codestring if c in '0123456789')
            return super(ISBN._Renderer, self).build_codestring(cs)
    renderer = _Renderer
    

class Ean8(Barcode):
    """
    >>> bc = Ean8()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean8 object at ...>
    >>> print bc.render_ps_code('01335583') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 60 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (01335583) () ean8 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('01335583', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> #_.show()
    """
    codetype = 'ean8'
    aliases = ('ean_8', 'ean-8', 'ean 8')
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 8*7+4, DPI]
        default_options = dict(textyoffset=-4)
        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textmaxh = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [4, textyoffset-textsize, 7*7+8+textsize*0.6, textmaxh]
            else:
                return self.code_bbox
    renderer = _Renderer


class Ean5(Barcode):
    """
    >>> bc = Ean5()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean5 object at ...>
    >>> print bc.render_ps_code('90200') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 35 50
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (90200) () ean5 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('977147396801', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> #_.show()
    """
    codetype = 'ean5'
    aliases = ('ean_5', 'ean-5', 'ean 5')
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 5*7, 0.7*DPI]
        default_options = dict(textyoffset=0.7*DPI+1)
        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textminy = textyoffset
            textmaxy = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [13-9, textminy, (4-1)*9+13+textsize*0.6, textmaxy]
            else:
                return self.code_bbox
    renderer = _Renderer


class Ean2(Barcode):
    """
    >>> bc = Ean2()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Ean2 object at ...>
    >>> print bc.render_ps_code('05') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 14 50
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (05) () ean2 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('05', options=dict(includetext=None), scale=2, margin=0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> #_.show()
    """
    codetype = 'ean2'
    aliases = ('ean_2', 'ean-2', 'ean 2')
    class _Renderer(LinearCodeRenderer):
        code_bbox = [0, 0, 2*7, 0.7*DPI]
        default_options = dict(textyoffset=0.7*DPI+1)
        @property
        def text_bbox(self):
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 12)
            textminy = textyoffset
            textmaxy = textyoffset + textsize
            if self.lookup_option('includetext', False) is None:
                return [-9+13, textminy, 13+textsize*0.6, textmaxy]
            else:
                return self.code_bbox
    renderer = _Renderer




if __name__=="__main__":
    from doctest import testmod
    testmod()
