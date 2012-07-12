# -*- coding: utf-8 -*-
"""
    extract

    Extract messages from tornado templates

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import ast

from tornado import escape
from tornado.template import (_UNSET, _DEFAULT_AUTOESCAPE, _TemplateReader,
    _parse, _File, _Expression)


GETTEXT_FUNCTIONS = ('_', '_N', 'gettext', 'ngettext')


class DummyTemplate(object):
    """A template object just used to parse the template string.
    The class resembles tornado.Template but stops at parsing the file.
    """
    def __init__(self, template_string, name="<string>", loader=None,
                 compress_whitespace=None, autoescape=_UNSET):
        self.name = name
        self.compress_whitespace = True
        if autoescape is not _UNSET:
            self.autoescape = autoescape
        elif loader:
            self.autoescape = loader.autoescape
        else:
            self.autoescape = _DEFAULT_AUTOESCAPE
        self.namespace = loader.namespace if loader else {}
        reader = _TemplateReader(name, escape.native_str(template_string))
        self.file = _File(self, _parse(reader, self))


def walk(node):
    """
    Given a template node, walk over all its descendants

    >>> t = DummyTemplate("{{ _('Hello') }}")
    >>> len(list(walk(t.file)))
    3
    >>> t = DummyTemplate("{% if a %}{{ _('Hello') }}{% end %}")
    >>> len(list(walk(t.file)))
    5
    """
    for child in node.each_child():
        if child.each_child():
            for grandchild in walk(child):
                yield grandchild
        yield child


def extract_from_node(expression, gettext_functions=None):
    """Extract localizable strings from the given Template Expression

    :param expression: A node of type tornado.template._Expression
    :param gettext_functions: A list of gettext function names that should be
                              parsed from template
    :return: iterator returning tuple in the format babel wants
    """
    if gettext_functions is None:
        gettext_functions = GETTEXT_FUNCTIONS

    for node in ast.walk(ast.parse(expression.expression)):
        # Recursively walk through all descendant nodes 
        if isinstance(node, ast.Call):
            # If the type is a function call
            if not (
                    isinstance(node.func, ast.Name) and \
                    node.func.id in gettext_functions):
                continue

            strings = []
            for arg in node.args:
                if isinstance(arg, ast.Str):
                    strings.append(arg.s)
                else:
                    strings.append(None)

            for arg in node.keywords:
                strings.append(None)
            if node.starargs is not None:
                strings.append(None)
            if node.kwargs is not None:
                strings.append(None)

            if len(strings) == 1:
                strings, = strings
            else:
                strings = tuple(strings)

            yield expression.line, node.func.id, strings


def extract_tornado(fileobj, keywords, comment_tags, options):
    """Extract messages from Python source code.


    :param fileobj: the seekable, file-like object the messages should be
	            extracted from
    :param keywords: a list of keywords (i.e. function names) that should be
	            recognized as translation functions
    :param comment_tags: a list of translator tags to search for and include
	            in the results. (Not implemented yet)
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)`` tuples
    :rtype: ``iterator``
    """
    template = DummyTemplate(
        fileobj.read(),
        file.name or options.get('name', '<string>'),
    )

    for node in walk(template.file):
        if isinstance(node, _Expression):
            for lineno, func, message in extract_from_node(node):
                # TODO: Implement the comment feature, right now an empty 
                # iterable is returned
                yield lineno, func, message, []
