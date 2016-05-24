# coding: utf-8
from __future__ import print_function
import codecs, itertools
import re
from .base import Barcode, MatrixCodeRenderer, DPI
# import logging
# logging.basicConfig(level=logging.DEBUG)

SYMBOL_CAPACITIES = dict(
    fullcaps=dict(
        numeric=dict(
            L=[  41,   77,  127,  187,  255,  322,  370,  461,  552,  652,  # 1-L - 10-L
                772,  883, 1022, 1101, 1250, 1408, 1548, 1725, 1903, 2061,  # 11-L - 20-L
               2232, 2409, 2620, 2812, 3057, 3283, 3517, 3669, 3909, 4158,  # 21-L - 30-L
               4417, 4686, 4965, 5253, 5529, 5836, 6153, 6479, 6743, 7089], # 31-L - 40-L
            M=[  34,   63,  101,  149,  202,  255,  293,  365,  432,  513,  # 1-M - 10-M
                604,  691,  796,  871,  991, 1082, 1212, 1346, 1500, 1600,  # 11-M - 20-M
               1708, 1872, 2059, 2188, 2395, 2544, 2701, 2857, 3035, 3289,  # 21-M - 30-M
               3486, 3693, 3909, 4134, 4343, 4588, 4775, 5039, 5313, 5596], # 31-M - 40-M
            Q=[  27,   48,   77,  111,  144,  178,  207,  259,  312,  364,  # 1-Q - 10-Q
                427,  489,  580,  621,  703,  775,  876,  948, 1063, 1159,  # 11-Q - 20-Q
               1224, 1358, 1468, 1588, 1718, 1804, 1933, 2085, 2181, 2358,  # 21-Q - 30-Q
               2473, 2670, 2805, 2949, 3081, 3244, 3417, 3599, 3791, 3993], # 31-Q - 40-Q
            H=[  17,   34,   58,   82,  106,  139,  154,  202,  235,  288,  # 1-H - 10-H
                331,  374,  427,  468,  530,  602,  674,  746,  813,  919,  # 11-H - 20-H
                969, 1056, 1108, 1228, 1286, 1425, 1501, 1581, 1677, 1782,  # 21-H - 30-H
               1897, 2022, 2157, 2301, 2361, 2524, 2625, 2735, 2927, 3057], # 31-H - 40-H
            ),
        alphanumeric=dict(
            L=[  25,   47,   77,  114,  154,  195,  224,  279,  335,  395,  # 1-L - 10-L
                468,  535,  619,  667,  758,  854,  938, 1046, 1153, 1249,  # 11-L - 20-L
               1352, 1460, 1588, 1704, 1853, 1990, 2132, 2223, 2369, 2520,  # 21-L - 30-L
               2677, 2840, 3009, 3183, 3351, 3537, 3729, 3927, 4087, 4296], # 31-L - 40-L
            M=[20, 38, 61, 90, 122, 154, 178, 221, 262, 311, # 1-M - 10-M
               366, 419, 483, 528, 600, 656, 734, 816, 909, 970, # 11-M - 20-M
               1035, 1134, 1248, 1326, 1451, 1542, 1637, 1732, 1839, 1994, # 21-M - 30-M
               2113, 2238, 2369, 2506, 2632, 2780, 2894, 3054, 3220, 3391], # 31-M - 40-M
            Q=[16, 29, 47, 67, 87, 108, 125, 157, 189, 221, # 1-Q - 10-Q
               259, 296, 352, 376, 426, 470, 531, 574, 644, 702, # 11-Q - 20-Q
               742, 823, 890, 963, 1041, 1094, 1172, 1263, 1322, 1429, # 21-Q - 30-Q
               1499, 1618, 1700, 1787, 1867, 1966, 2071, 2181, 2298, 2420], # 31-Q - 40-Q
            H=[10, 20, 35, 50, 64, 84, 93, 122, 143, 174, # 1-H - 10-H
               200, 227, 259, 283, 321, 365, 408, 452, 493, 557, # 11-H - 20-H
               587, 640, 672, 744, 779, 864, 910, 958, 1016, 1080, # 21-H - 30-H
               1150, 1226, 1307, 1394, 1431, 1530, 1591, 1658, 1774, 1852], # 31-H - 40-H
            ),
        byte=dict(
            L=[17, 32, 53, 78, 106, 134, 154, 192, 230, 271, # 1-L - 10-L
               321, 367, 425, 458, 520, 586, 644, 718, 792, 858, # 11-L - 20-L
               929, 1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628, 1732, # 21-L - 30-L
               1840, 1952, 2068, 2188, 2303, 2431, 2563, 2699, 2809, 2953], # 31-L - 40-L
            M=[14, 26, 42, 62, 84, 106, 122, 152, 180, 213, # 1-M - 10-M
               251, 287, 331, 362, 412, 450, 504, 560, 624, 666, # 11-M - 20-M
               711, 779, 857, 911, 997, 1059, 1125, 1190, 1264, 1370, # 21-M - 30-M
               1452, 1538, 1628, 1722, 1809, 1911, 1989, 2099, 2213, 2331], # 31-M - 40-M
            Q=[11, 20, 32, 46, 60, 74, 86, 108, 130, 151, # 1-Q - 10-Q
               177, 203, 241, 258, 292, 322, 364, 394, 442, 482, # 11-Q - 20-Q
               509, 565, 611, 661, 715, 751, 805, 868, 908, 982, # 21-Q - 30-Q
               1030, 1112, 1168, 1228, 1283, 1351, 1423, 1499, 1579, 1663], # 31-Q - 40-Q
            H=[7, 14, 24, 34, 44, 58, 64, 84, 98, 119, # 1-H - 10-H
               137, 155, 177, 194, 220, 250, 280, 310, 338, 382, # 11-H - 20-H
               403, 439, 461, 511, 535, 593, 625, 658, 698, 742, # 21-H - 30-H
               790, 842, 898, 958, 983, 1051, 1093, 1139, 1219, 1273], # 31-H - 40-H
            ),
        kanji=dict(
            L=[10, 20, 32, 48, 65, 82, 95, 118, 141, 167, # 1-L - 10-L
               198, 226, 262, 282, 320, 361, 397, 442, 488, 528, # 11-L - 20-L
               572, 618, 672, 721, 784, 842, 902, 940, 1002, 1066, # 21-L - 30-L
               1132, 1201, 1273, 1347, 1417, 1496, 1577, 1661, 1729, 1817], # 31-L - 40-L
            M=[8, 16, 26, 38, 52, 65, 75, 93, 111, 131, # 1-M - 10-M
               155, 177, 204, 223, 254, 277, 310, 345, 384, 410, # 11-M - 20-M
               438, 480, 528, 561, 614, 652, 692, 732, 778, 843, # 21-M - 30-M
               894, 947, 1002, 1060, 1113, 1176, 1224, 1292, 1362, 1435], # 31-M - 40-M
            Q=[7, 12, 20, 28, 37, 45, 53, 66, 80, 93, # 1-Q - 10-Q
               109, 125, 149, 159, 180, 198, 224, 243, 272, 297, # 11-Q - 20-Q
               314, 348, 376, 407, 440, 462, 496, 534, 559, 604, # 21-Q - 30-Q
               634, 684, 719, 756, 790, 832, 876, 923, 972, 1024], # 31-Q - 40-Q
            H=[4, 8, 15, 21, 27, 36, 39, 52, 60, 74, # 1-H - 10-H
               85, 96, 109, 120, 136, 154, 173, 191, 208, 235, # 11-H - 20-H
               248, 270, 284, 315, 330, 365, 385, 405, 430, 457, # 21-H - 30-H
               486, 518, 553, 590, 605, 647, 673, 701, 750, 784], # 31-H - 40-H
            ),
        ),
    microcaps=dict(
        numeric=dict(
            L=[5, 10, 23, 35], M=[-1, 8, 18, 30 ],
            Q=[-1, -1, -1, 21], H=[-1, -1, -1, -1]),
        alphanumeric=dict(
            L=[-1, 6, 14, 21], M=[-1, 5, 11, 18],
            Q=[-1, -1, -1, 13], H=[-1, -1, -1, -1]),
        byte=dict(
            L=[-1, -1, 9, 15], M=[-1, -1, 7, 13],
            Q=[-1, -1, -1, 9], H=[-1, -1, -1, -1]),
        kanji=dict(
            L=[-1, -1, 6, 9], M=[-1, -1, 4, 8],
            Q=[-1, -1, -1, 5], H=[-1, -1, -1, -1]),
        ),
    )



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


def alphanumeric_or_raise(s):
    """raises ValueError if s is not alphanumeric.
    """
    try:
        match = re.match(r'[0-9A-Z $%*+./:].*', s)
    except TypeError:
        match = re.match(br'[0-9A-Z $%*+./:].*', s)
    if not match:
        raise ValueError


def kanji_decode(s):
    sjis = codecs.lookup('sjis').decode
    try:
        return sjis(s)
    except TypeError:
        return sjis(s.encode('utf8'))

def qrcode_metric(msgbits, encoding=None, format_='full', eclevel=None, version=None):
    """
    >>> qrcode_metric('', version=9)
    ('9', 53, 182)
    """
    # logging.debug('-'*30)
    # logging.debug('msgbits=%s' % (msgbits))
    if eclevel is None:
        eclevel = 'M' if format_=='full' else 'L'
    if encoding is None: # 'raw' encoding should be explicit.
        # do fallback test
        for enc, assertion, exc in [
            ('numeric', int, ValueError),
            ('alphanumeric', alphanumeric_or_raise, ValueError),
            ('kanji', kanji_decode, UnicodeDecodeError)]:
            try:
                assertion(msgbits)
                encoding = enc
                break
            except exc:
                pass
        else:
            encoding = 'byte'
    n_msgbits = 0
    if encoding=='raw': # as is
        n_msgbits = len(msgbits)
    else:
        n_chars = len(msgbits)
        if encoding=='numeric': # 3.3bits/ch
            di, mo = divmod(len(msgbits), 3)
            n_msgbits = 10*(di)+{0: 0, 1: 4, 2: 7}[mo]
        elif encoding=='alphanumeric': # 5.5bits/ch
            di, mo = divmod(len(msgbits), 2)
            n_msgbits = 11*(di/2)+{0: 0, 1:6}[mo]
        elif encoding=='kanji': # 13bits/ch
            n_chars /= 2
            n_msgbits = (len(msgbits)/2)*13
        elif encoding=='byte': # 8bits/ch
            n_msgbits = len(msgbits)*8
        else:
            raise ValueError('Unable to define message encoding.')
        caps_for_enc = (SYMBOL_CAPACITIES
                        .get('fullcaps' if format_=='full' else 'microcaps')
                        .get(encoding))
        if version is None:
            caps_for_eclv = caps_for_enc.get(eclevel)
            for i, cap in enumerate(caps_for_eclv):
                # logging.debug('lv=%d, n_chars %s cap %s' %(i+1, n_chars, cap))
                if n_chars<=cap:
                    # logging.debug('breaking lv=%d, n_chars %s <= cap %s' %(i+1, n_chars, cap))
                    break
            version = str(i+1)
            if format_=='micro':
                version = 'M'+version
        elif isinstance(version, int):
            version = str(version)
        version_idx = int(version.replace('M', ''))-1
        if eclevel=='L' and n_chars<=caps_for_enc['M'][version_idx]:
            eclevel='M'
        if eclevel=='M' and n_chars<=caps_for_enc['Q'][version_idx]:
            eclevel='Q'
        if eclevel=='Q' and n_chars<=caps_for_enc['H'][version_idx]:
            eclevel='H'

        encvals = dict(
            numeric=0, alphanumeric=1, byte=2, kanji=3)

        mids = dict(
            M1=[   '',    -1,    -1,    -1],
            M2=[  '0',   '1',    -1,    -1],
            M3=[ '00',  '01',  '10',  '11'],
            M4=['000', '001', '010', '011'])
        for i in range(40):
            mids[str(i+1)] = ['0001', '0010', '0100', '1000']

        mid = mids[version][encvals[encoding]]
            
        cc1to9 =   [10,  9,  8,  8]
        cc10to26 = [12, 11, 16, 10]
        cc27to40 = [14, 13, 16, 12]

        cclens = dict(
            M1=[3, -1, -1, -1],
            M2=[4, 3, -1, -1],
            M3=[5, 4, 4, 3],
            M4=[6, 5, 5, 4])
        for i in range(9):
            cclens[str(i+1)]=cc1to9
        for i in range(9, 26):
            cclens[str(i+1)]=cc10to26
        for i in range(27, 40):
            cclens[str(i+1)]=cc27to40
        
        cclen = cclens[version][encvals[encoding]]

        n_msgbits = len(mid)+cclen+n_msgbits
            
    # logging.debug('enc=%s fmt=%s eclv=%s ver=%s' % (encoding, format_, eclevel, version))
    ecval = 'LHQM'.index(eclevel)
    if version:
        version = str(version)
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
        if format_!=frmt:
            continue
        if version not in [None, vers]:
            continue
        if n_msgbits>dmod:
            continue
        break
    else:
        raise ValueError(u'No appropriate mode for %sbits enc=%s/fmt=%s/eclv=%s/ver=%s'
                         %(n_msgbits, encoding, format_, eclevel, version))
    # logging.debug(str([msgbits, n_msgbits, encoding, format_, eclevel, version]))
    return vers, int(size), int(dcws)


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


class QrCode(Barcode):
    """
    >>> bc = QrCode()
    >>> bc # doctest: +ELLIPSIS
    <....QrCode object at ...>
    >>> print(bc.render_ps_code('000100000010000000001100010101100110000110000', options=dict(encoding='raw'))) # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 0 42 42
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    <30303031303030303030313030303030303030303131303030313031303131303031313
     0303030313130303030>
    <656e636f64696e673d726177>
    /qrcode /uk.co.terryburton.bwipp findresource exec
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('000100000010000000001100010101100110000110000', options=dict(encoding='raw')) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('Kansai Python Users DevCamp 2009 Kyoto', options=dict(version=9, eclevel='M'), scale=1, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render('Kansai Python Users DevCamp 2009 Kyoto', scale=1, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render(QrCode._sample_kanji_string, options=dict(version=9, eclevel='M'), scale=1, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    >>> bc.render(QrCode._sample_kanji_string, scale=1, margin=1) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile ... at ...>
    >>> # _.show()
    """
    _sample_kanji_string = u'あいうえお'.encode('sjis')
    codetype = 'qrcode'
    aliases = ('qr', 'qr_code', 'qr-code', 'qr code')
    class _Renderer(MatrixCodeRenderer):
        """
        >>> print(QrCode._Renderer('qrcode', data_mode='digits').render_ps_code('01234567')) # doctest: +ELLIPSIS
        %!PS-Adobe-2.0
        ...
        <3031323334353637>
        <>
        /qrcode /uk.co.terryburton.bwipp findresource exec
        ...
        >>>
        """
        default_options = dict(
            MatrixCodeRenderer.default_options,
            encoding=None, raw=False, format='full', version=None, eclevel=None)

        def _code_bbox(self, codestring):
            """
            >>> QrCode._Renderer({})._code_bbox(
            ...   '000100000010000000001100010101100110000110000')
            (0, 0, 50, 50)
            """
            mode = self.render_options.get('data_mode', 'raw')
            version = self.lookup_option('version')
            format_ = self.lookup_option('format')
            eclevel = self.lookup_option('eclevel')
            encoding = self.lookup_option('encoding')
            vers, size, dcws = qrcode_metric(codestring, encoding, format_, eclevel, version)
            return (0, 0, int(size*2*DPI/72.0), int(size*2*DPI/72.0))

        def build_params(self, codestring):
            r"""
            >>> import pprint
            >>> bits = '000100000010000000001100010101100110000110000'
            >>> pprint.pprint(QrCode._Renderer({}).build_params(bits), width=131)
            {'bbox': '0 0 50 50',
             'codestring': '<30303031303030303030313030303030303030303131303030313031303131303031313\n 0303030313130303030>',
             'codetype': {},
             'options': '<>',
             'xscale': 1.0,
             'yscale': 1.0}
            """
            params = super(QrCode._Renderer, self).build_params(codestring)
            cbbox = self._code_bbox(codestring)
            params['bbox'] = '%d %d %d %d' %(self._boundingbox(cbbox, cbbox))
            return params
        
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()

