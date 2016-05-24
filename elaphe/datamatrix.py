# coding: utf-8
from __future__ import print_function
import itertools, re
from .base import Barcode, MatrixCodeRenderer, DPI
from .util import cap_unescape

metrics = (
    # rows cols regh regv rscw rsbl
    [ 10,  10,    1,    1,    5,  1],
    [ 12,  12,    1,    1,    7,  1],
    [ 14,  14,    1,    1,   10,  1],
    [ 16,  16,    1,    1,   12,  1],
    [ 18,  18,    1,    1,   14,  1],
    [ 20,  20,    1,    1,   18,  1],
    [ 22,  22,    1,    1,   20,  1],
    [ 24,  24,    1,    1,   24,  1],
    [ 26,  26,    1,    1,   28,  1],
    [ 32,  32,    2,    2,   36,  1],
    [ 36,  36,    2,    2,   42,  1],
    [ 40,  40,    2,    2,   48,  1],
    [ 44,  44,    2,    2,   56,  1],
    [ 48,  48,    2,    2,   68,  1],
    [ 52,  52,    2,    2,   84,  1],
    [ 64,  64,    4,    4,  112,  1],
    [ 72,  72,    4,    4,  144,  1],
    [ 80,  80,    4,    4,  192,  1],
    [ 88,  88,    4,    4,  224,  1],
    [ 96,  96,    4,    4,  272,  1],
    [104, 104,    4,    4,  336,  1],
    [120, 120,    6,    6,  408,  1],
    [132, 132,    6,    6,  496,  1],
    [144, 144,    6,    6,  620,  1],
    [  8,  18,    1,    1,    7,  1],
    [  8,  32,    1,    2,   11,  1],
    [ 12,  26,    1,    1,   14,  1],
    [ 12,  36,    1,    2,   18,  1],
    [ 16,  36,    1,    2,   24,  1],
    [ 16,  48,    1,    2,   28,  1],
    )


class DataMatrix(Barcode):
    """
    >>> bc = DataMatrix()
    >>> bc # doctest: +ELLIPSIS
    <....DataMatrix object at ...>
    >>> print(bc.render_ps_code('This is Data Matrix')) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 40 40
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <546869732069732044617461204d6174726978>
    <>
    /datamatrix /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('This is Data Matrix') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('This is ^068ata Matrix') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('Fixed size', options=dict(rows=48, columns=48)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('Rectangular', options=dict(rows=16, columns=48)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> #_.show()
    >>> bc.render('^098^099^100^142^164^186^101^102^103^104^105',
    ...     options=dict(raw=True)) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'datamatrix'
    aliases = ('data matrix', 'data-matrix', 'data_matrix')
    class _Renderer(MatrixCodeRenderer):
        default_options = dict(
            MatrixCodeRenderer.default_options,
            rows=0, columns=0, prefix='', encoding='ascii', raw=False, parse=False,
            parsefnc=False)

        def _code_bbox(self, codestring):
            rows = self.lookup_option('rows')
            columns = self.lookup_option('columns')
            prefix = self.lookup_option('prefix')
            encoding = self.lookup_option('encoding')
            raw = self.lookup_option('raw')
            parse = self.lookup_option('parse')
            parsefnc = self.lookup_option('parse')
            if parse==True:
                codestring = cap_unescape(codestring)
            premaps = dict(FNC1=[232], PROG=[234], MAC5=[236], MAC6=[237])
            precws = premaps.get(prefix, [])
            prelen = len(precws)
            barlen = len(codestring)
            cw_length = 0
            if raw==True:
                encoding = 'raw'
            if encoding=='raw':
                cw_length = barlen/4+prelen
            elif encoding=='ascii':
                # BY sub(), codestring NO LONGER CARRY ACTUAL MESSAGE.
                if parsefnc==True:
                    cw_length += len(re.findall(r'(?<!\^)\^FNC1', codestring))
                    codestring = re.sub(r'(?<!\^)\^FNC1', '', codestring)
                    codestring.replace('^^', '^')
                residue = codestring
                while residue:
                    if residue[:2].isdigit():
                        cw_length+=2
                        residue = residue[2:]
                        continue
                    elif residue[0].isdigit():
                        cw_length+=1
                        residue = residue[1:]
                        continue
                    elif ord(residue[0])<128:
                        cw_length+=1
                        residue = residue[1:]
                        continue
                    else:
                        cw_length+=2
                        residue = residue[1:]
            elif encoding in ['c40', 'text', 'x12']:
                enc_props = dict(
                    c40=dict(
                        mode=230, eightbits=True,
                        charmap=(
                            '404142434445464748494a4b4c4d4e4f'
                            '505152535455565758595a5b5c5d5e5f'
                            '03808182838485868788898a8b8c8d8e'
                            '0405060708090a0b0c0d8f9091929394'
                            '950e0f101112131415161718191a1b1c'
                            '1d1e1f2021222324252627969798999a'
                            'c0c1c2c3c4c5c6c7c8c9cacbcccdcecf'
                            'd0d1d2d3d4d5d6d7d8d9dadbdcdddedf')),
                    text=dict(
                        mode=239, eightbits=True,
                        charmap=(
                            '404142434445464748494a4b4c4d4e4f'
                            '505152535455565758595a5b5c5d5e5f'
                            '03808182838485868788898a8b8c8d8e'
                            '0405060708090a0b0c0d8f9091929394'
                            '95c1c2c3c4c5c6c7c8c9cacbcccdcecf'
                            'd0d1d2d3d4d5d6d7d8d9da969798999a'
                            'c00e0f101112131415161718191a1b1c'
                            '1d1e1f2021222324252627dbdcdddedf')),
                    x12=dict(
                        mode=238, eightbits=False,
                        parsefnc=False,
                        charmap=(
                            'ffffffffffffffffffffffffff00ffff'
                            'ffffffffffffffffffffffffffffffff'
                            '03ffffffffffffffffff01ffffffffff'
                            '0405060708090a0b0c0dffffffff02ff'
                            'ff0e0f101112131415161718191a1b1c'
                            '1d1e1f2021222324252627ffffffffff'
                            'ffffffffffffffffffffffffffffffff'
                            'ffffffffffffffffffffffffffffffff')))
                parsefnc = enc_props.get('parsefnc', parsefnc)
                mode = enc_props.get('mode')
                eightbits = enc_props.get('eightbits')
                charmap = enc_props.get('charmap')
                if parsefnc==True:
                    cw_length += 2*len(
                        re.findall(r'(?<!\^)\^FNC1', codestring))
                    codestring = re.sub(r'(?<!\^)\^FNC1', '', codestring)
                    codestring.replace('^^', '^')
                residue = codestring
                while residue:
                    ch, residue = residue[:1], residue[1:]
                    if eightbits and ord(ch)>127:
                        cw_length+=2
                        continue
                    if 0<ord(ch)<128:
                        m_ord = int(charmap[ord(ch)*2:ord(ch)*2+2], 16)
                        if m_ord!=255:
                            if ((m_ord>>6)-1)!=0:
                                cw_length+=1
                            else:
                                pass
                        else:
                            raise ValueError(
                                'Invalid character in X12 encoding')
                # pad for triples
                if (cw_length%3):
                    cw_length+=(3-cw_length%3)
                # triples->2bytes
                cw_length = (cw_length/3)*2+prelen+1
            else:
                raise ValueError('invalid encoding (%s).' %encoding)
            ucols = rows
            urows = columns
            for rows, cols, regh, regv, rscw, rsbl in metrics:
                mrows = rows - (2*regh)
                mcols = cols - (2*regv)
                rrows = mrows//regh
                rcols = mcols//regv
                ncws = mrows*mcols//8-rscw
                if cw_length>ncws:
                    continue
                if urows and urows!=rows:
                    continue
                if ucols and ucols!=cols:
                    continue
                break
            return (0, 0, DPI*cols/72.0*2, DPI*rows/72.0*2)

        def build_params(self, codestring):
            """
            >>> import pprint
            >>> pprint.pprint(DataMatrix._Renderer(()).build_params('abcd'))
            {'bbox': '0 0 24 24',
             'codestring': '<61626364>',
             'codetype': (),
             'options': '<>',
             'xscale': 1.0,
             'yscale': 1.0}
            """
            params = super(DataMatrix._Renderer, self).build_params(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(
                self._code_bbox(codestring), self._code_bbox(codestring)))
            return params
    renderer = _Renderer

    

if __name__=="__main__":
    from doctest import testmod
    testmod()

