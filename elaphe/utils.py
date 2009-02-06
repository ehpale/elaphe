# coding: utf-8

from os.path import abspath, dirname, join as pathjoin
import re

# default barcode.ps path and distiller regexp.
DEFAULT_PS_CODE_PATH = pathjoin(
    dirname(abspath(__file__)), 'postscriptbarcode', 'barcode.ps')
DEFAULT_DISTILL_RE = re.compile(r'% --BEGIN TEMPLATE--(.+)% --END TEMPLATE--', re.S)

def to_ps(obj, escape_string=True):
    """Converts object into postscript literal"""
    if isinstance(obj, str) and escape_string:
        return '(%s)' %obj
    elif isinstance(obj, bool):
        return {True: 'true', False: 'false'}[obj]
    else:
        return str(obj)


def ps_optstring(d, none=lambda x: ' () ', empty=lambda x: ' () '):
    """Converts dictionary into ps string in barcode.ps specific format.

    >>> ps_optstring(dict(purpose='seekagrail', color='yellow', ni=None))
    ' (color=yellow ni purpose=seekagrail) '
    >>> ps_optstring(dict())
    ' () '
    >>> ps_optstring(None)
    ' () '
    """
    if d is None:
        return none(d)
    elif d:
        return ' ' + to_ps(' '.join(
            ('%s'%(k)+{True: '', False: '=%s'%to_ps(v, escape_string=False)}[v is None])
            for k, v in d.items())) + ' '
    else:
        return empty(d)

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


if __name__=="__main__":
    from doctest import testmod
    testmod()
