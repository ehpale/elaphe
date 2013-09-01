# coding: utf-8
import unittest
import module_doctests


def suite():
    return unittest.TestSuite([
        module_doctests.suite()])

def run():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__=='__main__':
    run()
