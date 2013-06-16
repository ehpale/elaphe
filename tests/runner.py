# coding: utf-8
import unittest
import module_doctests


def suite():
    return unittest.TestSuite([
        module_doctests.suite()])

unittest.TextTestRunner(verbosity=2).run(suite())
