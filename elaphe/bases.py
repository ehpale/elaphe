# coding: utf-8
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
from PIL.EpsImagePlugin import EpsImageFile

import config, utils

DPI = 72

class Renderer(object):
    default_options = {}

    def __init__(self, codetype, options=None, **kw):
        self.codetype = codetype
        self.options = dict(self.__class__.default_options)
        if options:
            self.options.update(options)
        if kw:
            self.options.update(kw)

    def text_bbox(self):
        """
        >>> r = Renderer('ean13')
        >>> r.text_bbox() == r.code_bbox()
        True
        """
        return self.code_bbox()

    def code_bbox(self):
        """
        >>> r = Renderer('ean13')
        >>> r.text_bbox() == [0, 0, DPI, DPI]
        True
        """
        return [0, 0, DPI, DPI]

    def left_margin(self):
        return 0

    def right_margin(self):
        return 0

    def top_margin(self):
        return 0

    def bottom_margin(self):
        return 0

    def boundingbox(self):
        text_lbx, text_lby, text_rtx, text_rty = self.text_bbox()
        code_lbx, code_lby, code_rtx, code_rty = self.code_bbox()
        return (min(text_lbx, code_lbx)-self.left_margin(),
                min(text_lby, code_lby)-self.bottom_margin(),
                max(text_rtx, code_rtx)+self.right_margin(),
                max(text_rty, code_rty)+self.top_margin())
        
    def render_ps_code(self, codestring):
        """
        >>> print Renderer('ean13').render_ps_code('977147396801') # doctest: +ELLIPSIS
        %!PS-Adobe-2.0
        %%Pages: (attend)
        %%Creator: Elaphe powered by barcode.ps
        %%BoundingBox: 0 0 72 72
        %%LanguageLevel: 2
        %%EndComments
        <BLANKLINE>
        <BLANKLINE>
        <BLANKLINE>
        % --BEGIN ENCODER ean13--
        ...
        % --END DISPATCHER--
        <BLANKLINE>
        <BLANKLINE>
        <BLANKLINE>
        gsave
        0 0 moveto
        (977147396801) () ean13 barcode
        grestore
        showpage
        <BLANKLINE>
        """
        params = {}
        params['bbox'] = "%d %d %d %d" %self.boundingbox()
        params['codestring'] = utils.to_ps(codestring)
        params['options'] = utils.ps_optstring(self.options)
        params['codetype'] = self.codetype
        return config.PS_CODE_TEMPLATE %(params)

    def render(self, codestring):
        """
        >>> Renderer('ean13').render('977147396801') # doctest: +ELLIPSIS
        <PIL.EpsImagePlugin.EpsImageFile instance at ...>
        """
        ps_code_buf = self.render_ps_code(codestring)
        return EpsImageFile(StringIO.StringIO(ps_code_buf))


class LinearCodeRenderer(Renderer):

    default_options = dict(
        barcolor=None,
        includetext=False,
        textcolor=None,
        textxalign=None,
        textyalign=None,
        textfont='Courier',
        textsize=10,
        textxoffset=0,
        textyoffset=0,
        bordercolor=None,
        backgroundcolor=None,
        inkspread=0.15,
        width=0,
        barratio=1,
        spaceratio=1,
        showborder=False,
        borderleft=10,
        borderright=10,
        bordertop=1,
        borderbottom=1,
        borderwidth=0.5,
        guardwhitespace=False,
        guardleftpos=0,
        guardrightpos=0,
        guardwidth=6,
        guardheight=7,
        )

    @property
    def boundingbox(self):
        return (0, 0, DPI, 100)
    
    
class MatrixCodeRenderer(object):
    def __init__(self):
        self.options = dict(
            
           )


class Barcode(object):
    """Base class of barcode renderers. The codetype defaults to ean13.
    """
    codetype = 'ean13'
    aliases = ('EAN-13', 'EAN_13', 'JAN')
    registry = {}
    default_options = {}
    renderer = Renderer
    @classmethod
    def update_codetype_registry(cls):
        # update registry
        for subclass in filter(lambda c: getattr(c, '__abstract', False) is False,
                               cls.__subclasses__()):
            cls.registry.update({subclass.codetype.lower(): subclass})
            if hasattr(subclass, 'aliases'):
                cls.registry.update(
                    dict((alias.lower(), subclass) for alias in subclass.aliases))

    @classmethod
    def resolve_codetype(cls, codetype):
        return cls.registry.get(codetype.lower())

    def get_renderer(self, options=None, **kw):
        return self.renderer(self.codetype, options, **kw)

    def render_ps_code(self, codestring, options=None, **kw):
        renderer = self.get_renderer(options, **kw)
        return renderer.render_ps_code(codestring)

    def render(self, codestring, options=None, **kw):
        renderer = self.get_renderer(options, **kw)
        return renderer.render(codestring)


if __name__=="__main__":
    from doctest import testmod
    testmod()
