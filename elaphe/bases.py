# coding: utf-8
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
from PIL.EpsImagePlugin import EpsImageFile

import config, utils

class BarcodeRenderer(object):
    """Base class of barcode renderers. The codetype defaults to ean13.
    """
    codetype = 'ean13'
    aliases = ('EAN-13', 'EAN_13', 'JAN')
    registry = {}
    default_options = {}
    @classmethod
    def update_renderer_registry(cls):
        # update registry
        for subclass in filter(lambda c: getattr(c, '__abstract', False) is False,
                               cls.__subclasses__()):
            cls.registry.update({subclass.codetype.lower(): subclass})
            if hasattr(subclass, 'aliases'):
                cls.registry.update(
                    dict((alias.lower(), subclass) for alias in subclass.aliases))

    @classmethod
    def resolve_renderer(cls, codetype):
        return cls.registry.get(codetype.lower())

    def render_ps_code(self, codestring, bbox=(-20, -20, 164, 92), options=None, **kw):
        """
        >>> print BarcodeRenderer().render_ps_code('977147396801', (-20, -20, 92, 164)) # doctest: +ELLIPSIS
        %!PS-Adobe-2.0
        %%Pages: (attend)
        %%Creator: Elaphe powered by barcode.ps
        %%BoundingBox: -20 -20 92 164
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
        (977147396801) ean13 barcode
        grestore
        showpage
        <BLANKLINE>
        """
        params = {}
        params['bbox'] = "%d %d %d %d" %bbox
        params['codestring'] = utils.ps_string(codestring)
        opts = dict(self.default_options)
        opts.update(options or {})
        params['options'] = utils.ps_optstring(opts)
        params['codetype'] = self.codetype
        params.update(kw)
        return config.PS_CODE_TEMPLATE %(params)

    def render(self, codestring, options=None, **kw):
        """
        >>> BarcodeRenderer().render('977147396801') # doctest: +ELLIPSIS
        <PIL.EpsImagePlugin.EpsImageFile instance at ...>
        """
        ps_code_buf = self.render_ps_code(codestring, options=options, **kw)
        return EpsImageFile(StringIO.StringIO(ps_code_buf))


class LinearBarcode(object):
    pass
    

if __name__=="__main__":
    from doctest import testmod
    testmod()
