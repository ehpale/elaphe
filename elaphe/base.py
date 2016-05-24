# coding: utf-8

from __future__ import print_function
import io
from PIL.EpsImagePlugin import EpsImageFile
from . import util

__all__=['DPI', 'Renderer', 'LinearCodeRenderer',
         'MatrixCodeRenderer', 'Barcode']

DPI = 72.0


def fb_lookup(dic, keys, default):
    """Do dict-lookup for multiple key, returning the first hit.
    """
    for key in keys:
        if key in dic:
            return dic[key]
    else:
        return default
    

class Renderer(object):
    """Base renderer implementation.
    """
    # The default_options is used as a fallback of renderer options.
    # 'Abstract' subclass such as LinearRenderer may override this as::
    #     default_options = dict(superclass.default_options, **kwargs)
    default_options = dict(
        # input processing
        parse=False,
        parsefnc=False,
        raw=False,
        # symbol dimensions
        height=0,
        width=0,
        )

    def __init__(self, codetype, options=None, **kw):
        self.codetype = codetype
        self.options = options
        self.render_options = kw

    def lookup_option(self, key, default=None):
        return (self.options or {}).get(
            key, getattr(self, 'default_options').get(key, default))

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
        return util.ps_hex_str(codestring)
        
    def build_options_string(self, options):
        return util.dict_to_optstring(options, raw=False)

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
        >>> print(Renderer('foo').render_ps_code('BAR')) # doctest: +ELLIPSIS
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
        <424152>
        <>
        /foo /uk.co.terryburton.bwipp findresource exec
        grestore
        showpage
        <BLANKLINE>
        """
        return util.PS_CODE_TEMPLATE %(self.build_params(codestring))

    def render(self, codestring):
        """
        >>> Renderer('foo').render('977147396801') # doctest: +ELLIPSIS
        <PIL.EpsImagePlugin.EpsImageFile ... at ...>
        """
        ps_code_buf = self.render_ps_code(codestring)
        try:
            f = io.BytesIO(ps_code_buf)
        except TypeError:
            f = io.BytesIO(ps_code_buf.encode('utf8'))
        return EpsImageFile(f)


class LinearCodeRenderer(Renderer):
    default_options = dict(
        Renderer.default_options,
        # check digits
        includecheck=False,
        includecheckintext=False,
        # bar properties
        inkspread=0.15,
        # text properties
        includetext=False,
        textfont='Courier',
        textsize=10,
        textgaps=0,
        # text positioning
        textxalign=None,
        textyalign=None,
        textxoffset=0,
        textyoffset=0,
        # border properties
        showborder=False,
        borderwidth=0.5,
        borderleft=10,
        borderright=10,
        bordertop=1,
        borderbottom=1,
        # symbol colors
        barcolor=None,
        backgroundcolor=None,
        textcolor=None,
        bordercolor=None,
        # EAN/UPC add-on
        addontextfont='Courier',
        addontextsize=10,
        addontextxoffset=0,
        addontextyoffset=0,
        # EAN/UPC guards
        guardwhitespace=False,
        guardwidth=6,
        guardheight=7,
        guardleftpos=0,
        guardrightpos=0,
        guardleftypos=0,
        guardrightypos=0,
        # attic
        barratio=1,
        spaceratio=1,
        )

    
class MatrixCodeRenderer(Renderer):
    default_options = dict(
        Renderer.default_options,
        # symbol colors
        color=None,
        backgrroundcolor=None,
        )


class Barcode(object):
    """Base class of barcode renderers.

    >>> print(Barcode().render_ps_code('')) # doctest: +ELLIPSIS
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
    <>
    <>
    / /uk.co.terryburton.bwipp findresource exec
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
