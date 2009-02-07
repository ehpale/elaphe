# coding: utf-8
import itertools
from bases import Barcode, MatrixCodeRenderer, DPI

def qrcode_size(version):
    is_micro, size = False, 0
    if isinstance(version, str):
        if version[:1].lower() == 'm':
            is_miscro = True
            return True, 9+2*int(version[1:])
    return False, 17+4*int(version)

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
  [(8, 255)]
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
    <__main__.QrCode object at ...>
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
    >>> bc.render('Kansai Python Users DevCamp 2009 Kyoto', options=dict(version=9, eclevel='M'), margin=10, data_mode='8bits') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    codetype = 'qrcode'
    aliases = ('qr', 'qr_code', 'qr-code', 'qrcode')
    class _Renderer(MatrixCodeRenderer):
        """
        >>> print QrCode._Renderer({}, data_mode='digits').render_ps_code('01234567') # doctest: +ELLIPSIS
        %!PS-Adobe-2.0
        ...
        (000100000010000000001100010101100110000110000) () {} barcode
        ...
        >>>
        """

        def build_codestring(self, codestring):
            mode = self.render_options.get('data_mode', 'raw')
            return super(QrCode._Renderer, self).build_codestring(
                qr_encode(codestring, mode))
        
        @property
        def code_bbox(self):
            is_miscro, size = qrcode_size(self.lookup_option('version', 9))
            return [0, 0, size*2, size*2]
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()
