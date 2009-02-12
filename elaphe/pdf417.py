# coding: utf-8
import itertools, math
from bases import Barcode, MatrixCodeRenderer, DPI

class Pdf417(Barcode):
    """
    >>> bc = Pdf417()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Pdf417 object at ...>
    >>> print bc.render_ps_code('^453^178^121^239') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 103 30
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (^453^178^121^239) () pdf417 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('^453^178^121^239', options=dict(columns=2, rows=10), margin=10, scale=1.0) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'pdf417'
    aliases = ()
    class _Renderer(MatrixCodeRenderer):
            
        def _code_bbox(self, codestring):
            compact = self.lookup_option('compact', False)
            columns = self.lookup_option('columns', 2)
            rowmult = self.lookup_option('rowmult', 3)
            rows = self.lookup_option('rows', 10)
            eclevel = self.lookup_option('eclevel', -1)
            m = len(codestring)/4
            if eclevel==-1:
                if m<=40:
                    eclevel = 2
                elif 41<=m<=160:
                    eclevel = 3
                elif 161<=m<=320:
                    eclevel = 4
                else: # m>=321
                    eclevel = 5
            maxeclevel = int(math.log(928-1-m)/math.log(2))-1
            if eclevel>maxeclevel:
                eclevel = maxeclevel
            k = 2**(eclevel+1)
            if 1<=columns<=30:
                c = columns
            else:
                raise ValueError
            r = int(math.ceil((m+k+1)/(1.0*columns)))
            if r<rows and rows<=90:
                r = rows
            if r<3:
                r = 3
            maxeclevel = int(math.log(c*r-1-m)/math.log(2))-1
            if maxeclevel>eclevel:
                eclevel = maxeclevel
                k = 2**(eclevel+1)
            if compact:
                rwid = 17*c+17+17+1
            else:
                rwid = 17*c+17+17+17+17+1
            return (0, 0, DPI*rwid/72.0, DPI*(r/72.0)*rowmult)

        def build_params(self, codestring):
            """
            >>> Pdf417._Renderer({}).build_params('abcd')
            {'yscale': 1.0, 'codestring': '(abcd)', 'bbox': '0 0 103 30', 'codetype': {}, 'xscale': 1.0, 'options': ' () '}
            """
            params = super(Pdf417._Renderer, self).build_params(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(
                self._code_bbox(codestring), self._code_bbox(codestring)))
            return params
    renderer = _Renderer
    

if __name__=="__main__":
    from doctest import testmod
    testmod()

