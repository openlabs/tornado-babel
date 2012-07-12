# -*- coding: utf-8 -*-
"""

    Babel localisation support for Tornado

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages

setup(
    name = "Tornado-Babel",
    version = "0.1",
    packages = find_packages(),

    install_requires = [
        "tornado",
        "babel",
        "speaklater",
    ],

    author = "Openlabs Technologies & Consulting (P) Limited",
    author_email = "info@openlabs.co.in",
    description = "Babel localisation support for Torando",
    license = "BSD",
    keywords = "tornado locale babel localisation",
    url = "https://github.com/openlabs/tornado-babel",
    test_suite = "tests.test_all",

    entry_points="""
    [babel.extractors]
    tornado = tornadobabel.extract:extract_tornado
    """,
)
