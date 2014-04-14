# coding: utf-8
from __future__ import print_function
import itertools
from .base import Barcode, MatrixCodeRenderer, DPI

class MaxiCode(Barcode):
    """
    >>> bc = MaxiCode()
    >>> bc # doctest: +ELLIPSIS
    <....MaxiCode object at ...>
    >>> print(bc.render_ps_code('This is MaxiCode')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 74 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <54686973206973204d617869436f6465>
    <>
    /maxicode /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('This is MaxiCode') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('This is Maxi^067ode', options=dict(parse=True)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render(
    ...     '152382802^029840^029001^0291Z00004951^029UPSN^02906X610'
    ...     '^029159^0291234567^0291/1^029^029Y^029634 ALPHA DR^029'
    ...     'PITTSBURGH^029PA^029^004',
    ...     options=dict(mode=2, parse=True)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render(
    ...     'ABC123^029840^029001^0291Z00004951^029UPSN^02906X610'
    ...     '^029159^0291234567^0291/1^029^029Y^029634 ALPHA DR^029'
    ...     'PITTSBURGH^029PA^029^004',
    ...     options=dict(mode=3, parse=True)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render(
    ...     '[)>^03001^02996152382802^029840^029001^0291Z00004951'
    ...     '^029UPSN^02906X610^029159^0291234567^0291/1^029^029Y'
    ...     '^029634 ALPHA DR^029PITTSBURGH^029PA^029^004',
    ...     options=dict(mode=2, parse=True)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'maxicode'
    aliases = ('maxi-code', 'maxi code', 'maxi_code', 'maxi')
    class _Renderer(MatrixCodeRenderer):
        default_options=dict(
            MatrixCodeRenderer.default_options,
            mode=4, sam=-1)

        @property
        def code_bbox(self):
            col, row = [v*2.4945 for v in (29+0.5*2, 32*0.8661+0.5774*2)]
            return (0, 0, col, row) 
    renderer = _Renderer

if __name__=="__main__":
    from doctest import testmod
    testmod()
