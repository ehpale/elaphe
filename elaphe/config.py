# coding: utf-8
"""
>>> print BARCODE_PS_CODE_PATH # doctest: +ELLIPSIS
<BLANKLINE>
<BLANKLINE>
%% --BEGIN ENCODER ean13--
%% --DESC: EAN-13
%% --EXAM: 977147396801
%% --EXOP: includetext guardwhitespace
%% --RNDR: renlinear
...
%% --BEGIN DISPATCHER--
/barcode {
    0 begin
    dup (ren) get cvx exec 
    end
} bind def
/barcode load 0 1 dict put
%% --END DISPATCHER--
<BLANKLINE>
<BLANKLINE>
>>> print PS_CODE_TEMPLATE # doctest: +ELLIPSIS
%%!PS-Adobe-2.0
%%%%Pages: (attend)
%%%%Creator: Elaphe powered by barcode.ps
%%%%BoundingBox: %(bbox)s
%%%%LanguageLevel: 2
%%%%EndComments
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>
%% --BEGIN ENCODER ean13--
...
%% --END DISPATCHER--
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>
gsave
0 0 moveto
%(codestring)s%(options)s%(codetype)s barcode
grestore
showpage
<BLANKLINE>
"""
from utils import *

BARCODE_PS_CODE_PATH = distill_ps_code()
PS_CODE_TEMPLATE = init_ps_code_template()

if __name__=="__main__":
    from doctest import testmod
    testmod()
