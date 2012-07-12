# -*- coding: utf-8 -*-
"""
    test_locale

    Test the method in the locale usage

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import os
import unittest

from tornado import web
from tornado import testing
from tornadobabel import locale
from tornadobabel.mixin import TornadoBabelMixin


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')


class Indexi18nHandler(TornadoBabelMixin, web.RequestHandler):
    def get_user_locale(self):
        """
        This locale handler is a bit old fashioned and picks up locale from
        the argument in the URL
        """
        _locale = locale.get(self.get_argument('locale', 'en_US'))
        return _locale

    def get(self):
        self.render('index.html')


class TestLocale(testing.AsyncHTTPTestCase):
    def get_app(self):
        test_dir = os.path.abspath(
            os.path.dirname(__file__)
        )
        locale.load_gettext_translations(
            os.path.join(test_dir, 'locales'), 'messages'
        )
        return web.Application([
            ('/', IndexHandler),
            ('/i18n', Indexi18nHandler),
        ])

    def test_0010_locales(self):
        self.assertTrue("es_ES" in locale._supported_locales)
        self.assertTrue("fr_FR" in locale._supported_locales)

        es_ES = locale.get('es_ES')
        self.assertEqual(es_ES.translate('Welcome'), "bienvenido")

    def test_without_i18n(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Welcome\n")

    def test_with_i18n(self):
        response = self.fetch('/i18n')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "Welcome\n")

        response = self.fetch('/i18n?locale=fr_FR')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenu\n")

        response = self.fetch('/i18n?locale=es_ES')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "bienvenido\n")


if __name__ == "__main__":
    unittest.main()
