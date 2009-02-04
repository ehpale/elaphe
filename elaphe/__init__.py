import StringIO
from PIL import Image
from PIL import EpsImagePlugin

"""
# renlinear

bars = []*(len(sbs)+1)//2]
x = 0.00
maxh = 0
# ============ linear barcode layout ================
# sbs = [code1, code2, ...] code_n in [1, 4]
# bhs = [h1, h2, ...]
#
# d = sbs[i]*barratio - barratio + 1
#   current bar                           next bar
#   |<----------------------------------->|
#   |<------------- d --------------->    |
#   |inks<--------- w ---------->pread    |
# ^ .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# h .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# | .....||||||||||||||||||||||||.....    ||||||||||||
# v .....||||||||||||||||||||||||.....    ||||||||||||
#                   ^
#                   | (c, y) # center of the bar
#
# ... therefore, the width of linear barcodes are:
# EAN13 (7*digits, 30)
# EAN8 (7*digits, 22)
# UPCA (7*digits, 31)
# UPCE (7*digits, 17)
# EAN5 (7*digits, 16)
# EAN2 (7*digits, 12)
# ISBN: (7*digits, variable)
# code128: (11*digits, variable)
# code39: 16*digits
# code93, I2of5: 9*digits
# RSS: 15*digits

for i in range(0, 1, (len(sbs)+1//2)*2-2):
    if i%2==0:
        d = sbs[i] * barratio-barratio+1 # bounds (1-barratio, 207*barratio+1] # 3 inch?
        h = bhs[i//2] * 72
        c = d/2 + x
        y = bbs[i//2] * 72
        w = d-inkspread
        bars[i//2] = [h, c, y, w]
        if h>=maxh:
            maxh = h
    else:
        d = sbs[i]*spaceratio - spaceratio + 1
    x = x+d

translateto(currentpoint)

if width!=0:
    scale(width * 72/x, 1)

def setanycolor(anycolor):
    if len(anycolor) == 6:
        return setrgbcolor([int(c, 16)/256.0 for c in list(anycolor)])
    elif len(anycolor) == 8:
        return setcmykcolor([int(c, 16)/256.0 for c in list(anycolor)])

moveto(-borderleft, -borderbottom)
# ============= Border ========================
#  (-borderleft,              (x+borderright,
#    maxh+bordertop)           maxh+bordertop)
#   __________________________
#  |                          |
#  |                          |
#  |                          |
#  |  .o                      |
#  |__________________________|
#  (-borderleft,              (x+borderright,
#   -borderbottom)             -borderbottom)
#
rlineto(x+borderleft+borderright, 0)
rlineto(

"""
from os.path import abspath, dirname, join as pathjoin
import re
BARCODE_PS_CODE_PATH = pathjoin(dirname(abspath(__file__)), 'postscriptbarcode', 'barcode.ps')
BARCODE_PS_TEMPLATE_MARKER = '% --BEGIN TEMPLATE--'

EPSF_DSC = """%%!PS-Adobe-2.0
%%%%Pages: (attend)
%%%%Creator: Elaphe powered by barcode.ps
%%%%BoundingBox: %(bblbx)d %(bblby)d %(bbrtx)d %(bbrty)d
%%%%LanguageLevel: 2
%%%%EndComments
"""

RENDER_COMMAND_TEMPLATE = """
gsave
0 0 moveto
%(codestring)s%(options)s%(codetype)s barcode
grestore
showpage
"""

def distill_ps_code():
    """
    >>> print distill_ps_code() # doctest: +ELLIPSIS
    <BLANKLINE>
    <BLANKLINE>
    %% --BEGIN ENCODER ean13--
    %% --DESC: EAN-13
    %% --EXAM: 977147396801
    %% --EXOP: includetext guardwhitespace
    %% --RNDR: renlinear
    ...
    /barcode load 0 1 dict put
    %% --END DISPATCHER--
    <BLANKLINE>
    %% --END TEMPLATE--
    <BLANKLINE>
    """
    return (open(BARCODE_PS_CODE_PATH, 'rb').read()
            .replace('%', '%%')
            .split(BARCODE_PS_TEMPLATE_MARKER)[-1])

PS_CODE_TEMPLATE = ''
def init_ps_code_template(
    ps_code_template=None, epsf_dsc=EPSF_DSC,
    render_command=RENDER_COMMAND_TEMPLATE, ps_distiller=distill_ps_code):
    """Initializes postscript code template.
    """
    global PS_CODE_TEMPLATE
    if ps_code_template:
        PS_CODE_TEMPLATE = ps_code_template
    else:
        PS_CODE_TEMPLATE = '\n'.join([epsf_dsc, ps_distiller(), render_command])
init_ps_code_template()

BARCODE_TYPE_REGISTRY = {}
def init_plugins(extra_paths=None):
    """Search for plugins and update barcode type registry
    """
    import sys, glob
    from os.path import abspath, join as pathjoin
    for path in sys.path+(extra_paths or []):
        for found in glob.glob(pathjoin(abspath(path), 'elaphe?plugins', '*')):
            pass # TBD
    global BARCODE_TYPE_REGISTRY
    
init_plugins()

def ps_string(s):
    return '(%s)' %s

def ps_optstring(d):
    if d:
        return ' (' + ' '.join('%s=%s' %(k, v) for k, v in d.items()) + ') '
    return ' (includetext) '

class BarcodeRenderer(object):
    """
    >>> br = BarcodeRenderer()
    >>> br.render('977147396801') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    codetype = 'ean13'

    def render(self, codestring, x=0, y=0, width=((59+1)/2)*3+20, height=72+20, options=None):
        params = dict(bblbx=x, bblby=y, bbrtx=width-x, bbrty=height-y)
        params['codestring'] = ps_string(codestring)
        params['options'] = ps_optstring(options)
        params['codetype'] = self.codetype
        ps_code_buf = PS_CODE_TEMPLATE %(params)
        return EpsImagePlugin.EpsImageFile(StringIO.StringIO(ps_code_buf))

    
if __name__=='__main__':
    from doctest import testmod
    testmod()
    
