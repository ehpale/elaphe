# coding: utf-8
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
from PIL.EpsImagePlugin import EpsImageFile

import config, utils


class BarcodeRenderer(object):
    """
    """
    codetype = 'ean13'

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
        params['options'] = utils.ps_optstring(options)
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


if __name__=="__main__":
    from doctest import testmod
    testmod()
