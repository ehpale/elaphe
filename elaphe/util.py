# coding: utf-8
from __future__ import print_function
from os.path import abspath, dirname, join as pathjoin
from binascii import hexlify
from textwrap import TextWrapper
import re

__all__ = ['DEFAULT_PS_CODE_PATH', 'DEFAULT_DISTILL_RE',
           'to_ps', 'cap_unescape', 'dict_to_optstring', 'distill_ps_code',
           'DEFAULT_EPSF_DSC_TEMPLATE', 'DEFAULT_RENDER_COMMAND_TEMPLATE',
           'init_ps_code_template', 'BARCODE_PS_CODE_PATH', 'PS_CODE_TEMPLATE']


# default barcode.ps path and distiller regexp.
DEFAULT_PS_CODE_PATH = pathjoin(
    dirname(abspath(__file__)), 'postscriptbarcode', 'barcode.ps')
DEFAULT_DISTILL_RE = re.compile(r'% --BEGIN TEMPLATE--(.+)% --END TEMPLATE--', re.S)


def _bin(n):
    """
    >>> _bin(0), _bin(1), _bin(63), _bin(4096)
    ('0', '1', '111111', '1000000000000')
    """
    return str(n) if n<=1 else _bin(n>>1) + str(n&1)
try:
    bin
except NameError:
    bin = lambda n: '0b'+_bin(n)

def zf_bin(n, width):
    """Zero-filled bin() of specified width.

    >>> zf_bin(1, 8)
    '00000001'
    >>> zf_bin(255, 8)
    '11111111'
    >>> zf_bin(256, 8)
    '00000000'
    """
    return bin(n)[2:].zfill(width)[0-width:]


_cap_escape_re = re.compile(r'^\^\d\d\d')
def cap_unescape(msg):
    """
    >>> cap_unescape('This is ^065ztec Code')
    'This is Aztec Code'
    
    """
    bits = []
    while msg:
        if _cap_escape_re.search(msg):
            oct_ord, msg = msg[1:4], msg[4:]
            bits.append(chr(int(oct_ord, 10)%256))
        else:
            bits.append(msg[0])
            msg = msg[1:]
    return ''.join(bits)


def to_ps(obj, parlen=False):
    """Converts object into postscript literal

    >>> to_ps(None)
    'null'
    >>> to_ps(123)
    '123'
    >>> to_ps(456.78)
    '456.78'
    >>> to_ps(True), to_ps(False)
    ('true', 'false')
    >>> to_ps('foo bar baz')
    'foo bar baz'
    >>> to_ps('foo bar baz', parlen=True)
    '(foo bar baz)'
    
    """
    if isinstance(obj, str):
        ret = '%s' %obj
        if parlen:
            ret = '(%s)' % ret
    elif isinstance(obj, bool):
        ret = {True: 'true', False: 'false'}[obj]
    elif isinstance(obj, type(None)):
        ret = 'null'
    else:
        ret = str(obj)
    return ret


def ps_hex_str(s):
    """
    
    >>> print(ps_hex_str('test testtesttesttest test test testtesttest test \\n'
    ...                  ' sdfojsodfj oij 3240987u098rusipdjf948325u test'))
    <74657374207465737474657374746573747465737420746573742074657374207465737
     474657374746573742074657374200a207364666f6a736f64666a206f696a2033323430
     393837753039387275736970646a66393438333235752074657374>
    """
    try:
        hexlified = hexlify(s)
    except TypeError:
        hexlified = hexlify(s.encode('utf8'))

    if isinstance(hexlified, bytes):
        hexlified = hexlified.decode('ascii')
    wrapped = '<{0}>'.format(hexlified)
    return TextWrapper(subsequent_indent=' ', width=72).fill(wrapped)


def dict_to_optstring(d, none=lambda x: '<>', empty=lambda x: '<>',
                      raw_none=lambda x: '()', raw_empty=lambda x: '()',
                      raw=True):
    """Converts dictionary into ps string in barcode.ps specific format.
    >>> from collections import OrderedDict as odict
    >>> dict_to_optstring(odict([
    ...     ('color','yellow'),
    ...     ('purpose', 'seekagrail'),
    ...     ('spam', True),
    ...     ('egg', False),
    ... ]), raw=True)
    '(color=yellow purpose=seekagrail spam)'
    >>> dict_to_optstring(dict(), raw=True)
    '()'
    >>> dict_to_optstring(None, raw=True)
    '()'
    >>> dict_to_optstring(odict([
    ...     ('color','yellow'),
    ...     ('purpose', 'seekagrail'),
    ...     ('spam', True),
    ...     ('egg', False),
    ... ]), raw=False)
    '<636f6c6f723d79656c6c6f7720707572706f73653d7365656b61677261696c207370616\\n d>'
    >>> dict_to_optstring(dict(), raw=False)
    '<>'
    >>> dict_to_optstring(None, raw=False)
    '<>'
    """
    none_ = none
    empty_ = empty
    if raw:
        none_ = raw_none
        empty_ = raw_empty
    if d is None:
        return none_(d)
    elif d:
        ret = ' '.join(
            (key + {True: '', False:'=%s' % to_ps(value)}[value is True])
            for key, value in list(d.items()) if not value is False)
        if raw:
            return '('+ret+')'
        else:
            return ps_hex_str(ret)
    else:
        return empty_(d)


def distill_ps_code(path_to_ps_code=DEFAULT_PS_CODE_PATH,
                    distill_regexp=DEFAULT_DISTILL_RE):
    """
    Distills barcode procedure code blocks with given path and regexp.

    >>> print(distill_ps_code()) # doctest: +ELLIPSIS
    <BLANKLINE>
    <BLANKLINE>
    %% --BEGIN RESOURCE preamble--
    %%%%BeginResource: Category uk.co.terryburton.bwipp 0.0 0 0 0
    %%%%BeginData:          5 ASCII Lines
    ...
    %%%%EndData
    %%%%EndResource
    %% --END ENCODER hibccodablockf--
    <BLANKLINE>
    <BLANKLINE>
    """
    return distill_regexp.findall(
        open(path_to_ps_code, 'r').read())[0].replace('%', '%%')


DEFAULT_EPSF_DSC_TEMPLATE = """%%!PS-Adobe-2.0
%%%%Pages: (attend)
%%%%Creator: Elaphe powered by barcode.ps
%%%%BoundingBox: %(bbox)s
%%%%LanguageLevel: 2
%%%%EndComments
"""
DEFAULT_RENDER_COMMAND_TEMPLATE = """
gsave
0 0 moveto
%(xscale)f %(yscale)f scale
%(codestring)s
%(options)s
/%(codetype)s /uk.co.terryburton.bwipp findresource exec
grestore
showpage
"""

def init_ps_code_template(epsf_dsc_template=DEFAULT_EPSF_DSC_TEMPLATE,
                          render_command_template=DEFAULT_RENDER_COMMAND_TEMPLATE,
                          ps_code_distiller=distill_ps_code):
    """Initializes postscript code template.
    """
    return '\n'.join([epsf_dsc_template, ps_code_distiller(), render_command_template])


BARCODE_PS_CODE_PATH = distill_ps_code()
PS_CODE_TEMPLATE = init_ps_code_template()


if __name__=="__main__":
    from doctest import testmod
    testmod()

