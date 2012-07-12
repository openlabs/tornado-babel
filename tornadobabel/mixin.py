# -*- coding: utf-8 -*-
"""
    mixin

    A mixin class that could be used to use tornadobabel instaed of the
    default tornado requesthandler locale.

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from speaklater import is_lazy_string, make_lazy_string
from tornadobabel import locale


def make_lazy_gettext(lookup_func):
    """Creates a lazy gettext function dispatches to a gettext
    function as returned by `lookup_func`.

    :copyright: (c) 2010 by Armin Ronacher.

    Example:

    >>> translations = {u'Yes': u'Ja'}
    >>> lazy_gettext = make_lazy_gettext(lambda: translations.get)
    >>> x = lazy_gettext(u'Yes')
    >>> x
    lu'Ja'
    >>> translations[u'Yes'] = u'Si'
    >>> x
    lu'Si'
    """
    def lazy_gettext(string, *args, **kwargs):
        if is_lazy_string(string):
            return string
        return make_lazy_string(lookup_func(), string, *args, **kwargs)
    return lazy_gettext


class TornadoBabelMixin(object):
    """A Mixin class that could be used with the request handler to override
    the default tornado.locales with tornadobabel.locale, when the browser
    locale is used.

    If your application handles locales, then you should implement the
    `get_user_locale` method.
    """

    @property
    def _(self):
        """
        A helper to easily get lazy version ugettext
        """
        return make_lazy_gettext(lambda: self.locale.translate)

    def get_browser_locale(self, default="en_US"):
        """Determines the user's locale from Accept-Language header.

        See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
        """
        if "Accept-Language" in self.request.headers:
            languages = self.request.headers["Accept-Language"].split(",")
            locales = []
            for language in languages:
                parts = language.strip().split(";")
                if len(parts) > 1 and parts[1].startswith("q="):
                    try:
                        score = float(parts[1][2:])
                    except (ValueError, TypeError):
                        score = 0.0
                else:
                    score = 1.0
                locales.append((parts[0], score))
            if locales:
                locales.sort(key=lambda (l, s): s, reverse=True)
                codes = [l[0] for l in locales]
                return locale.get(*codes)
        return locale.get(default)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
