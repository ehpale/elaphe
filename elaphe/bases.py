# coding: utf-8

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from PIL.EpsImagePlugin import EpsImageFile
import utils

__all__=['DPI', 'Renderer', 'LinearCodeRenderer', 'MatrixCodeRenderer', 'Barcode']

DPI = 72.0

def fb_lookup(dic, keys, default):
    """Dictionary lookup falls back over keys.
    """
    for key in keys:
        if key in dic:
            return dic[key]
    else:
        return default
    

class Renderer(object):
    """Base renderer implementation.
    """
    # Values in default_options are used as a fallback of renderer option.
    # Abstract subclass should override, substational renderers not.
    # To instant override, do as new = dict(superclass.default_options, **kwargs).
    default_options = dict()

    def __init__(self, codetype, options=None, **kw):
        self.codetype = codetype
        self.options = options
        self.render_options = kw

    def lookup_option(self, key, default=None):
        fb_value = getattr(self, 'default_options').get(key, default)
        if self.options:
            return self.options.get(key, fb_value)
        return fb_value

    @property
    def text_bbox(self):
        """
        >>> r = Renderer('ean13')
        >>> r.text_bbox == r.code_bbox
        True
        """
        return self.code_bbox

    @property
    def code_bbox(self):
        """
        >>> r = Renderer('ean13')
        >>> r.text_bbox == [0, 0, DPI, DPI]
        True
        """
        return [0, 0, DPI, DPI]

    @property
    def left_margin(self):
        return fb_lookup(self.render_options, ('left_margin', 'margin'), 0)

    @property
    def right_margin(self):
        return fb_lookup(self.render_options, ('right_margin', 'margin'), 0)

    @property
    def top_margin(self):
        return fb_lookup(self.render_options, ('top_margin', 'margin'), 0)

    @property
    def bottom_margin(self):
        return fb_lookup(self.render_options, ('bottom_margin', 'margin'), 0)

    @property
    def x_scale(self):
        scale = fb_lookup(self.render_options, ('scale',), 1.0)
        if isinstance(scale, tuple):
            scale = scale[0]
        return scale

    @property
    def y_scale(self):
        scale = fb_lookup(self.render_options, ('scale',), 1.0)
        if isinstance(scale, tuple):
            scale = scale[1]
        return scale

    @property
    def boundingbox(self):
        return self._boundingbox(self.code_bbox, self.text_bbox)

    def _boundingbox(self, code_bbox, text_bbox):
        text_lbx, text_lby, text_rtx, text_rty = text_bbox
        code_lbx, code_lby, code_rtx, code_rty = code_bbox
        return (self.x_scale*(min(text_lbx, code_lbx)-self.left_margin),
                self.y_scale*(min(text_lby, code_lby)-self.bottom_margin),
                self.x_scale*(max(text_rtx, code_rtx)+self.right_margin),
                self.y_scale*(max(text_rty, code_rty)+self.top_margin))

    def build_codestring(self, codestring):
        return utils.to_ps(codestring, parlen=True)
        
    def build_options_string(self, options):
        return utils.dict_to_optstring(options)

    def build_params(self, codestring):
        params = {}
        params['bbox'] = "%d %d %d %d" %self.boundingbox
        params['codestring'] = self.build_codestring(codestring)
        params['options'] = self.build_options_string(self.options)
        params['xscale'], params['yscale'] = self.x_scale, self.y_scale
        params['codetype'] = self.codetype
        return params

    def render_ps_code(self, codestring):
        """
        >>> print Renderer('foo').render_ps_code('977147396801') # doctest: +ELLIPSIS
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
        1.000000 1.000000 scale
        (977147396801) () foo barcode
        grestore
        showpage
        <BLANKLINE>
        """
        return utils.PS_CODE_TEMPLATE %(self.build_params(codestring))

    def render(self, codestring):
        """
        >>> Renderer('foo').render('977147396801') # doctest: +ELLIPSIS
        <PIL.EpsImagePlugin.EpsImageFile ... at ...>
        """
        ps_code_buf = self.render_ps_code(codestring)
        return EpsImageFile(StringIO.StringIO(ps_code_buf))


class LinearCodeRenderer(Renderer):
    default_options = dict(
        Renderer.default_options,
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

    
class MatrixCodeRenderer(Renderer):
    default_options = dict(
        Renderer.default_options,
        color=None,
        backgrroundcolor=None,
        height=1,
        width=1,
        )


class Barcode(object):
    """Base class of barcode renderers.

    >>> print Barcode().render_ps_code('') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 72 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    () ()  barcode
    grestore
    showpage
    <BLANKLINE>
    """
    codetype = ''
    aliases = ()
    registry = {}
    renderer = Renderer
    @classmethod
    def update_codetype_registry(cls):
        # update registry
        for subclass in cls.__subclasses__():
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

    # for debug
    def _get_build_params(self, codestring='', options=None, **kw):
        renderer = self.get_renderer(options, **kw)
        return renderer.build_params(codestring)
        

if __name__=="__main__":
    from doctest import testmod
    testmod()
