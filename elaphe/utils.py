# coding: utf-8

from os.path import abspath, dirname, join as pathjoin
import re

# default barcode.ps path and distiller regexp.
DEFAULT_PS_CODE_PATH = pathjoin(
    dirname(abspath(__file__)), 'postscriptbarcode', 'barcode.ps')
DEFAULT_DISTILL_RE = re.compile(r'% --BEGIN TEMPLATE--(.+)% --END TEMPLATE--', re.S)


def distill_ps_code(path_to_ps_code=DEFAULT_PS_CODE_PATH,
                    distill_regexp=DEFAULT_DISTILL_RE):
    """
    Distills barcode procedure code blocks with given path and regexp.

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
    <BLANKLINE>
    """
    return distill_regexp.findall(
        open(path_to_ps_code, 'rb').read())[0].replace('%', '%%')


def ps_string(s):
    """Converts string into ps string. Does not aware non-ascii.

    >>> ps_string('asdf')
    '(asdf)'
    """
    return '(%s)' %s


def ps_optstring(d):
    """Converts dictionary into ps string in barcode.ps specific format.

    >>> ps_optstring(dict(purpose='seekagrail', color='yellow'))
    ' (color=yellow purpose=seekagrail) '
    >>> ps_optstring(dict())
    ' () '
    >>> ps_optstring(None)
    ' '
    """
    if d is None:
        return ' '
    else:
        return ' (' + ' '.join(('%s'%(k)+('' if v is None else '=%s'%v)) for k, v in d.items()) + ') '

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
%(codestring)s%(options)s%(codetype)s barcode
grestore
showpage
"""

def init_ps_code_template(epsf_dsc_template=DEFAULT_EPSF_DSC_TEMPLATE,
                          render_command_template=DEFAULT_RENDER_COMMAND_TEMPLATE,
                          ps_code_distiller=distill_ps_code):
    """Initializes postscript code template.
    """
    return '\n'.join([epsf_dsc_template, ps_code_distiller(), render_command_template])

def init_plugins(extra_paths=None):
    """Search for plugins and update barcode type registry
    """
    ret = {}
    import sys, glob
    from os.path import abspath, join as pathjoin
    for path in sys.path+(extra_paths or []):
        for found in glob.glob(pathjoin(abspath(path), 'elaphe?plugins', '*')):
            pass # TBD
    return ret

if __name__=="__main__":
    from doctest import testmod
    testmod()
