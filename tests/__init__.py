# -*- coding: utf-8 -*-
"""
    __init__

    Test Suite for Tornado-Babel

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import sys
from unittest import TestSuite, TestLoader
sys.path.append('../')

from test_locale import TestLocale
from test_extract import TestExtract

def test_all():
    loader = TestLoader()
    suite = TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestLocale))
    suite.addTests(loader.loadTestsFromTestCase(TestExtract))
    return suite
