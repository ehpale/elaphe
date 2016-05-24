# coding: utf-8
from __future__ import print_function
from .base import Barcode, LinearCodeRenderer, DPI


class Rss14(Barcode):
    """
    >>> bc = Rss14()
    >>> bc # doctest: +ELLIPSIS
    <....Rss14 object at ...>
    >>> print(bc.render_ps_code('(01)24012345678905')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 97 33
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <283031293234303132333435363738393035>
    <>
    /databaromni /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('(01)24012345678905', scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('(01)24012345678905', options=dict(linkage=True, includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'databaromni'
    aliases = ('rss14', 'rss-14', 'rss_14', 'rss 14')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            height=33/72.0, textyoffset=-7, linkage=False)
        # SP(1),LG(1),D1(16),LF(15),D2(15),D4(15),R5(16),D3(16),SP(1),RG(1)
        _symbol_length = 1+1+16+15+15+15+16+16+1+1

        def _text_bbox(self, codestring):
            """
            >>> r = Rss14._Renderer({})
            >>> r._text_bbox('24012345678905')
            [0, 0, 97, 33]
            """
            if self.lookup_option('includetext'):
                cminx, cminy, cmaxx, cmaxy = self._code_bbox(codestring)
                textyoffset = self.lookup_option('textyoffset')
                textsize = self.lookup_option('textsize')
                textminy = textyoffset
                textmaxy = textyoffset + textsize
                cbox_center = (cminx+cmaxx)/2.0
                textminx = min(cminx, cbox_center-(len(codestring))*textsize*0.6/2.0)
                textmaxx = max(cmaxx, cbox_center+(len(codestring))*textsize*0.6/2.0)
                return [textminx, textyoffset, textmaxx, textyoffset+textsize]
            else:
                return self._code_bbox(codestring)

        def _code_bbox(self, codestring):
            """
            >>> r = Rss14._Renderer({})
            >>> r._code_bbox('24012345678905')
            [0, 0, 97, 33]
            """
            height = self.lookup_option('height')
            return [0, 0, int(self._symbol_length/72.0*DPI), int(height*DPI)]

        def build_params(self, codestring):
            params = super(Rss14._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
        
    renderer = _Renderer


class RssLimited(Barcode):
    """
    >>> bc = RssLimited()
    >>> bc # doctest: +ELLIPSIS
    <....RssLimited object at ...>
    >>> print(bc.render_ps_code('(01)15012345678907')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 74 10
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <283031293135303132333435363738393037>
    <>
    /databarlimited /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('(01)15012345678907', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'databarlimited'
    aliases = ('rsslimited', 'rss limited', 'rss_limited', 'rss-limited',
               'rss14limited', 'rss14 limited', 'rss14_limited', 'rss14-limited',)
    class _Renderer(Rss14._Renderer):
        default_options = dict(
            LinearCodeRenderer.default_options,
            textyoffset=-7, height=10/72.0)
        # SP(1),LG(1),LD(26),CC(18),RD(26),SP(1),RG(1)
        _symbol_length = 1+1+26+18+26+1+1
    renderer = _Renderer


# EXPERIMENTAL
class RssExpanded(Barcode):
    """
    >>> bc = RssExpanded()
    >>> bc # doctest: +ELLIPSIS
    <....RssExpanded object at ...>
    >>> print(bc.render_ps_code('(01)95012345678903(3103)000123')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 90 34
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <283031293935303132333435363738393033283331303329303030313233>
    <>
    /databarexpanded /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('(01)95012345678903(3103)000123', options=dict(includetext=True), scale=2, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show() # Broken!
    """
    codetype = 'databarexpanded'
    aliases = ('rssexpanded', 'rss expanded', 'rss_expanded', 'rss-expanded',
               'rss14expanded', 'rss14 expanded', 'rss14_expanded', 'rss14-expanded',)
    class _Renderer(Rss14._Renderer):
        default_options = dict(
            LinearCodeRenderer.default_options, height=34/72.0)
        def _code_bbox(self, codestring):
            """
            >>> r = RssExpanded._Renderer({})
            >>> r._code_bbox('000000010011001010100001000000010000')
            [0, 0, 105, 34]
            """
            height = self.lookup_option('height')
            return [0, 0, int(DPI*15*(len(codestring)//8+3)/72.0), int(height*DPI)]
        _text_bbox = _code_bbox
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
