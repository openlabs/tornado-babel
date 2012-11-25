# -*- coding: utf-8 -*-
"""
    test_merge

    Test the translations table mergin feature

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2012 by Centre Scientifique et Technique du Batiment
    :license: BSD, see LICENSE for more details.
"""
import os
import unittest

from tornado import web
from tornado import testing
from tornadobabel import locale
from tornadobabel.mixin import TornadoBabelMixin


class TestHandler(TornadoBabelMixin, web.RequestHandler):
    def get_user_locale(self):
        """
        This locale handler is a bit old fashioned and picks up locale from
        the argument in the URL
        """
        _locale = locale.get(self.get_argument('locale', 'en_US'))
        return _locale


class BaseHandler(TestHandler):
    def get(self):
        self.render('index.html')


class AdditHandler(TestHandler):
    def get(self):
        self.render('addit.html')


class MixedHandler(TestHandler):
    def get(self):
        self.render('mixed.html')


class TestMerge(testing.AsyncHTTPTestCase):
    def get_app(self):
        test_dir = os.path.abspath(
            os.path.dirname(__file__)
        )
        locale.load_gettext_translations(
            os.path.join(test_dir, 'locales'), 'messages'
        )
        locale.load_gettext_translations(
            os.path.join(test_dir, 'locales'), 'addit'
        )
        return web.Application([
            ('/', BaseHandler),
            ('/addit', AdditHandler),
            ('/mixed', MixedHandler),
        ])

    def test_base(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Welcome\n")

        response = self.fetch('/?locale=fr_FR')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenu\n")

        response = self.fetch('/?locale=es_ES')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenido\n")

    def test_addit(self):
        response = self.fetch('/addit')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Goodbye\n")

        response = self.fetch('/addit?locale=fr_FR')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Au revoir\n")

        response = self.fetch('/addit?locale=es_ES')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Adios\n")

    def test_mixed(self):
        response = self.fetch('/mixed')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Welcome / Goodbye\n")

        response = self.fetch('/mixed?locale=fr_FR')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenu / Au revoir\n")

        response = self.fetch('/mixed?locale=es_ES')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenido / Adios\n")


if __name__ == "__main__":
    unittest.main()
