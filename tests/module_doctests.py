# coding: utf-8
import doctest
import unittest
from importlib import import_module
from os import walk
from os.path import abspath, dirname, join

try:
    import elaphe
except ImportError:
    import sys
    sys.path.insert(0, dirname(dirname(abspath(__file__))))
    import elaphe
    
module_names = []
prefix = dirname(dirname(abspath(elaphe.__file__)))
for dp, dn, fns in walk(join(prefix, 'elaphe')):
    for fn in fns:
        if fn.endswith('.py'):
            module_names.append(
                dp[len(prefix):].strip('/').replace('/', '.')+'.'+fn[:-3])

def suite():
    suite_ = unittest.TestSuite()
    for module_name in module_names:
        suite_.addTest(doctest.DocTestSuite(import_module(module_name)))
    return suite_


if __name__=='__main__':
    unittest.TextTestRunner().run(suite())
