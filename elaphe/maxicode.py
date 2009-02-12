# coding: utf-8
import itertools
from bases import Barcode, MatrixCodeRenderer, DPI


class MaxiCode(Barcode):
    """
    >>> bc = MaxiCode()
    >>> bc # doctest: +ELLIPSIS
    <__main__.MaxiCode object at ...>
    >>> print bc.render_ps_code('^059^042^041^059^040^03001^02996152382802^029840^029001^0291Z00004951^029UPSN^02906X610^029159^0291234567^0291^0471^029^029Y^029634 ALPHA DR^029PITTSBURGH^029PA^030^062^004^063') # doctest: +ELLIPSIS
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
    (^059^042^041^059^040^03001^02996152382802^029840^029001^0291Z00004951^029UPSN^02906X610^029159^0291234567^0291^0471^029^029Y^029634 ALPHA DR^029PITTSBURGH^029PA^030^062^004^063) () maxicode barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('^059^042^041^059^040^03001^02996152382802^029840^029001^0291Z00004951^029UPSN^02906X610^029159^0291234567^0291^0471^029^029Y^029634 ALPHA DR^029PITTSBURGH^029PA^030^062^004^063', options=dict(mode=2), margin=10, scale=5.0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'maxicode'
    aliases = ()
    

if __name__=="__main__":
    from doctest import testmod
    testmod()
