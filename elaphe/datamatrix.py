# coding: utf-8
import itertools
from bases import Barcode, MatrixCodeRenderer, DPI

metrics = (
    # rows cols regh regv rscw rsbl
    [ 10,  10,    1,    1,    5],
    [ 12,  12,    1,    1,    7],
    [ 14,  14,    1,    1,   10],
    [ 16,  16,    1,    1,   12],
    [ 18,  18,    1,    1,   14],
    [ 20,  20,    1,    1,   18], 
    [ 22,  22,    1,    1,   20],
    [ 24,  24,    1,    1,   24],
    [ 26,  26,    1,    1,   28],
    [ 32,  32,    2,    2,   36],
    [ 36,  36,    2,    2,   42],
    [ 40,  40,    2,    2,   48],
    [ 44,  44,    2,    2,   56],
    [ 48,  48,    2,    2,   68],
    [ 52,  52,    2,    2,   84],
    [ 64,  64,    4,    4,  112],
    [ 72,  72,    4,    4,  144],
    [ 80,  80,    4,    4,  192],
    [ 88,  88,    4,    4,  224],
    [ 96,  96,    4,    4,  272],
    [104, 104,    4,    4,  336],
    [120, 120,    6,    6,  408],
    [132, 132,    6,    6,  496],
    [144, 144,    6,    6,  620],)


class DataMatrix(Barcode):
    """
    >>> bc = DataMatrix()
    >>> bc # doctest: +ELLIPSIS
    <....DataMatrix object at ...>
    >>> print bc.render_ps_code('^142^164^186') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 24 24
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (^142^164^186) () datamatrix barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('^142^164^186', options=dict(columns=32, rows=32), margin=1, scale=2.0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> #_.show()
    """
    codetype = 'datamatrix'
    aliases = ('data matrix', 'data-matrix', 'data_matrix')
    class _Renderer(MatrixCodeRenderer):
        default_options = dict(
            MatrixCodeRenderer.default_options,
            rows=0, columns=0)

        def _code_bbox(self, codestring):
            ucols = self.lookup_option('columns', 2)
            urows = self.lookup_option('rows', 10)
            for rows, cols, regh, regv, rscw in metrics:
                mrows = rows - (2*regh)
                mcols = cols - (2*regv)
                rrows = mrows//regh
                rcols = mcols//regv
                ncws = mrows*mcols//8-rscw
                if len(codestring)>ncws:
                    continue
                if urows and urows!=rows:
                    continue
                if ucols and ucols!=cols:
                    continue
                break
            return (0, 0, DPI*cols/72.0*1.5, DPI*rows/72.0*1.5)

        def build_params(self, codestring):
            """
            >>> DataMatrix._Renderer(()).build_params('abcd')
            {'yscale': 1.0, 'codestring': '(abcd)', 'bbox': '0 0 18 18', 'codetype': (), 'xscale': 1.0, 'options': ' () '}
            """
            params = super(DataMatrix._Renderer, self).build_params(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(
                self._code_bbox(codestring), self._code_bbox(codestring)))
            return params
    renderer = _Renderer

    

if __name__=="__main__":
    from doctest import testmod
    testmod()

