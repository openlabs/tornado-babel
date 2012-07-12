# -*- coding: utf-8 -*-
"""
    test_extract

    test Message extraction from template files

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import sys
sys.path.append('../')

from StringIO import StringIO
import unittest

from tornadobabel.extract import extract_tornado


class TestExtract(unittest.TestCase):
    def setUp(self):
        pass

    def test_extract(self):
        template = StringIO("""
        {{ _("Test String") }}
        {{ something }}
        {% block something %}{% end %}
        """)
        strings = list(extract_tornado(template, None, None, {}))
        self.assertEqual(len(strings), 1)

        # Ensure that the string is correct
        string, = strings
        self.assertEqual(string[0], 2)  # Line number
        self.assertEqual(string[1], '_')  # Function name
        self.assertEqual(string[2], "Test String")  # Translatable string

    def test_n_extract(self):
        template = StringIO("""
        {{ _("Test String") }}
        {{ _N("%(num)d apple", "%(num)d apples", count) }}
        {{ something }}
        {% block something %}{% end %}
        """)
        strings = list(extract_tornado(template, None, None, {}))
        self.assertEqual(len(strings), 2)

        # Ensure that the string is correct
        string = strings[1]
        self.assertEqual(string[0], 3)  # Line number
        self.assertEqual(string[1], '_N')  # Function name
        self.assertEqual(string[2], ('%(num)d apple', '%(num)d apples', None))

    def test_nested_extract(self):
        template = StringIO("""
        {% extends 'somethingelse.html' %}
        {% block abc %}
        {{ _("Test String") }}
        {% end %}
        """)

        strings = list(extract_tornado(template, None, None, {}))
        self.assertEqual(len(strings), 1)

        # Ensure that the string is correct
        string, = strings
        self.assertEqual(string[0], 4)  # Line number
        self.assertEqual(string[1], '_')  # Function name
        self.assertEqual(string[2], "Test String")  # Translatable string


if __name__ == "__main__":
    unittest.main()
