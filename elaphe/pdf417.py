# coding: utf-8
from __future__ import print_function
import itertools, math
from .base import Barcode, MatrixCodeRenderer, DPI
from .util import cap_unescape

class Pdf417(Barcode):
    """
    >>> bc = Pdf417()
    >>> bc # doctest: +ELLIPSIS
    <....Pdf417 object at ...>
    >>> print(bc.render_ps_code('PDF417')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 103 24
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <504446343137>
    <>
    /pdf417 /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('PDF417', options=dict()) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('P^068F417', options=dict(parse=True, columns=2, rows=15), scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('1234', options=dict(columns=2, rows=10), scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('A truncated PDF417', options=dict(columns=4, compact=True), scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('String error correction', options=dict(columns=2, eclevel=5), scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('^453^178^121^239', options=dict(raw=True, columns=2), scale=2) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    
    """
    codetype = 'pdf417'
    aliases = ('pdf-417', 'pdf_417', 'pdf 417')
    class _Renderer(MatrixCodeRenderer):
        default_options = dict(
            MatrixCodeRenderer.default_options,
            dontdraw=False, compact=False, eclevel=-1, columns=2, rows=0, rowmult=3,
            ccc=False, raw=False, parse=False)
            
        def _code_bbox(self, codestring):
            compact = self.lookup_option('compact')
            columns = self.lookup_option('columns')
            rowmult = self.lookup_option('rowmult')
            rows = self.lookup_option('rows')
            eclevel = self.lookup_option('eclevel')
            raw = self.lookup_option('raw')
            codestring = cap_unescape(codestring)
            m = 0
            if raw==False:
                blen = len(codestring)
                if blen%6==0:
                    m = (blen/6)*5+1
                else:
                    m = ((blen-blen%6)/6)*5+blen%6+1
            else:
                m = len(codestring)
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
            if columns==0:
                columns = int(round(math.sqrt((m+k)/3)))
            if 1<=columns<=30:
                c = columns
            else:
                raise ValueError(u'Column out of bound: %d.' %(columns))
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
            >>> import pprint
            >>> pprint.pprint(Pdf417._Renderer({}).build_params('abcd'))
            {'bbox': '0 0 103 21',
             'codestring': '<61626364>',
             'codetype': {},
             'options': '<>',
             'xscale': 1.0,
             'yscale': 1.0}
            """
            params = super(Pdf417._Renderer, self).build_params(codestring)
            cbbox = self._code_bbox(codestring)
            params['bbox'] = '%d %d %d %d' %self._boundingbox(cbbox, cbbox)
            return params
    renderer = _Renderer
    

if __name__=="__main__":
    from doctest import testmod
    testmod()

