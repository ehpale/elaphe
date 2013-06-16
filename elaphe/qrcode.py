# coding: utf-8
import itertools
from bases import Barcode, MatrixCodeRenderer, DPI

QRCODE_METRIC = [
    ["micro", "M1", 11, 98, 99, 36, [2, 99, 99, 99], [1, 0, 99, 99, 99, 99, 99, 99]],
    ["micro", "M2", 13, 98, 99, 80, [5, 6, 99, 99], [1, 0, 1, 0, 99, 99, 99, 99]],
    ["micro", "M3", 15, 98, 99, 132, [6, 8, 99, 99], [1, 0, 1, 0, 99, 99, 99, 99]],
    ["micro", "M4", 17, 98, 99, 192, [8, 10, 14, 99], [1, 0, 1, 0, 1, 0, 99, 99]],
    ["full", "1", 21, 98, 99, 208, [7, 10, 13, 17], [1, 0, 1, 0, 1, 0, 1, 0]],
    ["full", "2", 25, 18, 99, 359, [10, 16, 22, 28], [1, 0, 1, 0, 1, 0, 1, 0]],
    ["full", "3", 29, 22, 99, 567, [15, 26, 36, 44], [1, 0, 1, 0, 2, 0, 2, 0]],
    ["full", "4", 33, 26, 99, 807, [20, 36, 52, 64], [1, 0, 2, 0, 2, 0, 4, 0]],
    ["full", "5", 37, 30, 99, 1079, [26, 48, 72, 88], [1, 0, 2, 0, 2, 2, 2, 2]],
    ["full", "6", 41, 34, 99, 1383, [36, 64, 96, 112], [2, 0, 4, 0, 4, 0, 4, 0]],
    ["full", "7", 45, 22, 38, 1568, [40, 72, 108, 130], [2, 0, 4, 0, 2, 4, 4, 1]],
    ["full", "8", 49, 24, 42, 1936, [48, 88, 132, 156], [2, 0, 2, 2, 4, 2, 4, 2]],
    ["full", "9", 53, 26, 46, 2336, [60, 110, 160, 192], [2, 0, 3, 2, 4, 4, 4, 4]],
    ["full", "10", 57, 28, 50, 2768, [72, 130, 192, 224], [2, 2, 4, 1, 6, 2, 6, 2]],
    ["full", "11", 61, 30, 54, 3232, [80, 150, 224, 264], [4, 0, 1, 4, 4, 4, 3, 8]],
    ["full", "12", 65, 32, 58, 3728, [96, 176, 260, 308], [2, 2, 6, 2, 4, 6, 7, 4]],
    ["full", "13", 69, 34, 62, 4256, [104, 198, 288, 352], [4, 0, 8, 1, 8, 4, 12, 4]],
    ["full", "14", 73, 26, 46, 4651, [120, 216, 320, 384], [3, 1, 4, 5, 11, 5, 11, 5]],
    ["full", "15", 77, 26, 48, 5243, [132, 240, 360, 432], [5, 1, 5, 5, 5, 7, 11, 7]],
    ["full", "16", 81, 26, 50, 5867, [144, 280, 408, 480], [5, 1, 7, 3, 15, 2, 3, 13]],
    ["full", "17", 85, 30, 54, 6523, [168, 308, 448, 532], [1, 5, 10, 1, 1, 15, 2, 17]],
    ["full", "18", 89, 30, 56, 7211, [180, 338, 504, 588], [5, 1, 9, 4, 17, 1, 2, 19]],
    ["full", "19", 93, 30, 58, 7931, [196, 364, 546, 650], [3, 4, 3, 11, 17, 4, 9, 16]],
    ["full", "20", 97, 34, 62, 8683, [224, 416, 600, 700], [3, 5, 3, 13, 15, 5, 15, 10]],
    ["full", "21", 101, 28, 50, 9252, [224, 442, 644, 750], [4, 4, 17, 0, 17, 6, 19, 6]],
    ["full", "22", 105, 26, 50, 10068, [252, 476, 690, 816], [2, 7, 17, 0, 7, 16, 34, 0]],
    ["full", "23", 109, 30, 54, 10916, [270, 504, 750, 900], [4, 5, 4, 14, 11, 14, 16, 14]],
    ["full", "24", 113, 28, 54, 11796, [300, 560, 810, 960], [6, 4, 6, 14, 11, 16, 30, 2]],
    ["full", "25", 117, 32, 58, 12708, [312, 588, 870, 1050], [8, 4, 8, 13, 7, 22, 22, 13]],
    ["full", "26", 121, 30, 58, 13652, [336, 644, 952, 1110], [10, 2, 19, 4, 28, 6, 33, 4]],
    ["full", "27", 125, 34, 62, 14628, [360, 700, 1020, 1200], [8, 4, 22, 3, 8, 26, 12, 28]],
    ["full", "28", 129, 26, 50, 15371, [390, 728, 1050, 1260], [3, 10, 3, 23, 4, 31, 11, 31]],
    ["full", "29", 133, 30, 54, 16411, [420, 784, 1140, 1350], [7, 7, 21, 7, 1, 37, 19, 26]],
    ["full", "30", 137, 26, 52, 17483, [450, 812, 1200, 1440], [5, 10, 19, 10, 15, 25, 23, 25]],
    ["full", "31", 141, 30, 56, 18587, [480, 868, 1290, 1530], [13, 3, 2, 29, 42, 1, 23, 28]],
    ["full", "32", 145, 34, 60, 19723, [510, 924, 1350, 1620], [17, 0, 10, 23, 10, 35, 19, 35]],
    ["full", "33", 149, 30, 58, 20891, [540, 980, 1440, 1710], [17, 1, 14, 21, 29, 19, 11, 46]],
    ["full", "34", 153, 34, 62, 22091, [570, 1036, 1530, 1800], [13, 6, 14, 23, 44, 7, 59, 1]],
    ["full", "35", 157, 30, 54, 23008, [570, 1064, 1590, 1890], [12, 7, 12, 26, 39, 14, 22, 41]],
    ["full", "36", 161, 24, 50, 24272, [600, 1120, 1680, 1980], [6, 14, 6, 34, 46, 10, 2, 64]],
    ["full", "37", 165, 28, 54, 25568, [630, 1204, 1770, 2100], [17, 4, 29, 14, 49, 10, 24, 46]],
    ["full", "38", 169, 32, 58, 26896, [660, 1260, 1860, 2220], [4, 18, 13, 32, 48, 14, 42, 32]],
    ["full", "39", 173, 26, 54, 28256, [720, 1316, 1950, 2310], [20, 4, 40, 7, 43, 22, 10, 67]],
    ["full", "40", 177, 30, 58, 29648, [750, 1372, 2040, 2430], [19, 6, 18, 31, 34, 34, 20, 61]],
    ]

def qrcode_metric(msgbits, format='full', eclevel='M', version=None):
    """
    >>> qrcode_metric('', version=9)
    ('9', 53, 100)
    """
    if version:
        version = str(version)
    ecval = 'LHQM'.index(eclevel)
    for frmt, vers, size, asp2, asp3, nmod, ecws_list, ecb_list in QRCODE_METRIC:
        ncws, rbit = divmod(nmod, 8)
        if size in [11, 15]:
            ncws, rbit, lc4b = ncws+1, 0, True
        else:
            lc4b = False
        ecws = ecws_list[ecval]
        dcws = ncws-ecws
        dmod = dcws*8
        if lc4b:
            dmod = dmod-4
        ecb1 = ecb_list[ecval*2]
        ecb2 = ecb_list[ecval*2+1]
        dcpb = dcws//(ecb1+ecb2)
        ecpb = ncws//(ecb1+ecb2)-dcpb
        if version is None:
            if format!=frmt:
                continue
        else:
            if version!=vers:
                continue
        if len(msgbits)>dmod:
            continue
        break
    else:
        raise ValueError(u'No appropriate mode for %s, %s, %s, %s'
                         %(msgbits, format, eclevel, version))
    return vers, int(size), int(dcws)


def int_to_bitmask(number, digits=0, on='1', off='0'):
    """Converts integer to bitmask
    >>> int_to_bitmask(0, 0)
    ''
    >>> int_to_bitmask(100, 0)
    ''
    >>> int_to_bitmask(42, 6)
    '101010'
    >>> int_to_bitmask(42, 10)
    '0000101010'
    """
    return ''.join(str(((number>>i)&0x1)) for i in reversed(range(digits)))

ALNUM = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'
def decode_n_base(s, digits=1, mode='digits'):
    """Converts string representation of arbitrary based digits into integers.

    Returns tuples of number of digested digits and decoded value.

    >>> list(decode_n_base('ABC', mode='alnum'))
    [(11, 461), (6, 12)]
    >>> list(decode_n_base('300', mode='digits'))
    [(10, 300)]
    >>> list(decode_n_base('FF', mode='8bits'))
    [(8, 70), (8, 70)]
    """
    while True:
        if mode=='alnum':
            head, tail = s[:2], s[2:]
            if len(head)==2:
                yield (11, ALNUM.find(head[0])*45+ALNUM.find(head[1]))
            elif len(head)==1:
                yield (6, ALNUM.find(head[0]))
            else:
                break
        elif mode=='digits':
            head, tail = s[:3], s[3:]
            if len(head):
                yield (len(head)*3+1, int(head))
            else:
                break
        else:
            head, tail = s[:1], s[1:]
            if len(head):
                yield (8, ord(head))
            else:
                break
        s = tail
    return


def qr_encode(data, mode='raw', capacity=None):
    """
    >>> qr_encode('01234567', mode='digits')
    '000100000010000000001100010101100110000110000'
    """
    encode_buffer = []
    if mode=='raw':
        return data
    elif mode=='digits':
        # mode identifier
        encode_buffer.append((4, 1))
        # data length
        encode_buffer.append((10, len(data)))
        # data payload
        encode_buffer.extend(list(decode_n_base(data, mode='digits')))
    elif mode=='alnum':
        # mode identifier
        encode_buffer.append((4, 2))
        # data length
        encode_buffer.append((9, len(data)))
        # data payload
        encode_buffer.extend(list(decode_n_base(data, mode='alnum')))
    else: # 8bits mode
        # mode identifier
        encode_buffer.append((4, 4))
        # data length
        encode_buffer.append((8, len(data)))
        # data payload
        encode_buffer.extend(list(decode_n_base(data, mode='8bits')))
    # terminator
    encode_buffer.append((4, 0))
    encoded = ''.join(int_to_bitmask(value, digits)
                      for digits, value in encode_buffer)
    if capacity:
        encoded = encoded[:capacity]
    return encoded

class QrCode(Barcode):
    """
    >>> bc = QrCode()
    >>> bc # doctest: +ELLIPSIS
    <....QrCode object at ...>
    >>> print bc.render_ps_code('000100000010000000001100010101100110000110000') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 106 106
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (000100000010000000001100010101100110000110000) () qrcode barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('Kansai Python Users DevCamp 2009 Kyoto', options=dict(version=9, eclevel='M'), scale=1, margin=1, data_mode='8bits') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    codetype = 'qrcode'
    aliases = ('qr', 'qr_code', 'qr-code', 'qr code')
    class _Renderer(MatrixCodeRenderer):
        """
        >>> print QrCode._Renderer({}, data_mode='digits').render_ps_code('01234567') # doctest: +ELLIPSIS
        %!PS-Adobe-2.0
        ...
        (000100000010000000001100010101100110000110000) () {} barcode
        ...
        >>>
        """
        default_options = dict(
            MatrixCodeRenderer.default_options,
            format='full', version='9', eclevel='L')

        def build_codestring(self, codestring):
            mode = self.render_options.get('data_mode', 'raw')
            return super(QrCode._Renderer, self).build_codestring(
                qr_encode(codestring, mode))
        
        def _code_bbox(self, codestring):
            """
            >>> QrCode._Renderer({})._code_bbox(
            ...   '000100000010000000001100010101100110000110000')
            (0, 0, 106, 106)
            """
            mode = self.render_options.get('data_mode', 'raw')
            version = str(self.lookup_option('version'))
            format = self.lookup_option('format')
            eclevel = self.lookup_option('eclevel')
            msgbits = qrcode_metric(qr_encode(codestring, mode))
            vers, size, dcws = qrcode_metric(msgbits, format, eclevel, version)
            return (0, 0, size*2, size*2)

        def build_params(self, codestring):
            """
            >>> QrCode._Renderer({}).build_params(
            ...   '000100000010000000001100010101100110000110000')
            {'yscale': 1.0, 'codestring': '(000100000010000000001100010101100110000110000)', 'bbox': '0 0 106 106', 'codetype': {}, 'xscale': 1.0, 'options': ' () '}
            """
            params = super(QrCode._Renderer, self).build_params(codestring)
            cbbox = self._code_bbox(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(cbbox, cbbox))
            return params
        
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()

