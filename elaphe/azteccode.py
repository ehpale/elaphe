# coding: utf-8
import itertools, math
from bases import Barcode, MatrixCodeRenderer, DPI


AZTEC_CODE_METRICS = [
    # frmt      mlyr icap ncws  bpcw
    ["rune",    0,   0,   0,    6], # Special metric for rune symbols
    ["compact", 1,   1,   17,   6],
    ["full",    1,   1,   21,   6],
    ["compact", 2,   0,   40,   6],
    ["full",    2,   1,   48,   6],
    ["compact", 3,   0,   51,   8],
    ["full",    3,   1,   60,   8],
    ["compact", 4,   0,   76,   8],
    ["full",    4,   1,   88,   8],
    ["full",    5,   1,   120,  8],
    ["full",    6,   1,   156,  8],
    ["full",    7,   1,   196,  8],
    ["full",    8,   1,   240,  8],
    ["full",    9,   1,   230,  10],
    ["full",    10,  1,   272,  10],
    ["full",    11,  1,   316,  10],
    ["full",    12,  1,   364,  10],
    ["full",    13,  1,   416,  10],
    ["full",    14,  1,   470,  10],
    ["full",    15,  1,   528,  10],
    ["full",    16,  1,   588,  10],
    ["full",    17,  1,   652,  10],
    ["full",    18,  1,   720,  10],
    ["full",    19,  1,   790,  10],
    ["full",    20,  1,   864,  10],
    ["full",    21,  1,   940,  10],
    ["full",    22,  1,   1020, 10],
    ["full",    23,  0,   920,  12],
    ["full",    24,  0,   992,  12],
    ["full",    25,  0,   1066, 12],
    ["full",    26,  0,   1144, 12],
    ["full",    27,  0,   1224, 12],
    ["full",    28,  0,   1306, 12],
    ["full",    29,  0,   1392, 12],
    ["full",    30,  0,   1480, 12],
    ["full",    31,  0,   1570, 12],
    ["full",    32,  0,   1664, 12]]


class AztecCode(Barcode):
    """
    >>> bc = AztecCode()
    >>> bc # doctest: +ELLIPSIS
    <....AztecCode object at ...>
    >>> print bc.render_ps_code('00100111001000000101001101111000010100111100101000000110') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 30 30
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (00100111001000000101001101111000010100111100101000000110) () azteccode barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('00100111001000000101001101111000010100111100101000000110', margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'azteccode'
    aliases = ('aztec code', 'aztec-code', 'aztec_code', 'aztec')
    class _Renderer(MatrixCodeRenderer):
        default_options = dict(
            MatrixCodeRenderer.default_options,
            readerinit=False, layers=-1, eclevel=23, ecaddchars=3, format=None)
        def _code_bbox(self, codestring):
            format = self.lookup_option('format')
            if format!='rune':
                codelen = 0
            else:
                codelen = len(codestring)
            readerinit = self.lookup_option('readerinit')
            layers = self.lookup_option('layers')
            eclevel = self.lookup_option('eclevel')
            ecaddchars = self.lookup_option('ecaddchars')
            for frmt, mlyr, icap, ncws, bpcw in AZTEC_CODE_METRICS:
                if format and format!=frmt:
                    continue
                if readerinit and icap!=1:
                    continue
                if layers!=-1 and layers!=mlyr:
                    continue
                numecw = int(math.ceil(ncws*eclevel/100+ecaddchars))
                numdcw = ncws-numecw
                if math.ceil(codelen/bpcw)>numdcw:
                    continue
                break
            else:
                raise ValueError(u'No appropreate mode.')
            layers = mlyr
            format = frmt
            
            size = 9+layers*4+2
            if format=='full':
                size = ((13+layers*4)+2)+int((layers+10.5)/7.5-1)*2
            return (0, 0, DPI*size*2/72.0, DPI*size*2/72.0)

        def build_params(self, codestring):
            """
            >>> AztecCode._Renderer({}).build_params('abcd')
            {'yscale': 1.0, 'codestring': '(abcd)', 'bbox': '0 0 30 30', 'codetype': {}, 'xscale': 1.0, 'options': ' () '}
            """
            params = super(AztecCode._Renderer, self).build_params(codestring)
            cbbox = self._code_bbox(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(cbbox, cbbox))
            return params
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()

