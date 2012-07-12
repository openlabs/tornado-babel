# -*- coding: utf-8 -*-
"""
    Internationalisation using Babel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The locale support of tornado as such is pretty basic and does not offer
    support for merging translation catalogs and several other features most 
    multi language applications require.

    This module tries to retain the same API as that of tornado.locale while
    implement the required features with the support of babel.

    .. note::
        CSV Translations are not supported

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2009 by Facebook (Tornado Project)
    :license: BSD, see LICENSE for more details.
"""
import gettext
import logging
import os

from babel.support import Translations
from babel.core import Locale as BabelCoreLocale
from babel import dates, numbers

_default_locale = "en_US"
_translations = {}
_supported_locales = frozenset([_default_locale])
_use_gettext = False


def get(*locale_codes):
    """Returns the closest match for the given locale codes.

    We iterate over all given locale codes in order. If we have a tight
    or a loose match for the code (e.g., "en" for "en_US"), we return
    the locale. Otherwise we move to the next code in the list.

    By default we return en_US if no translations are found for any of
    the specified locales. You can change the default locale with
    set_default_locale() below.
    """
    return Locale.get_closest(*locale_codes)


def set_default_locale(code):
    """Sets the default locale, used in get_closest_locale().

    The default locale is assumed to be the language used for all strings
    in the system. The translations loaded from disk are mappings from
    the default locale to the destination locale. Consequently, you don't
    need to create a translation file for the default locale.
    """
    global _default_locale
    global _supported_locales
    _default_locale = code
    _supported_locales = frozenset(_translations.keys() + [_default_locale])


def load_gettext_translations(directory, domain):
    """Loads translations from gettext's locale tree"""
    global _translations
    global _supported_locales
    global _use_gettext
    _translations = {}
    for lang in os.listdir(directory):
        if lang.startswith('.'):
            continue  # skip .svn, etc
        if os.path.isfile(os.path.join(directory, lang)):
            continue
        try:
            # Load existing translation or Null Translations
            translation = _translations.get(lang, Translations.load())
            if isinstance(translation, gettext.NullTranslations):
                _translations[lang] = Translations.load(
                        directory, [lang], domain
                )
            else:
                _translations[lang].merge(
                        Translations.load(directory, [lang], domain)
                )
        except Exception, e:
            logging.error("Cannot load translation for '%s': %s", lang, str(e))
            continue
    _supported_locales = frozenset(_translations.keys() + [_default_locale])
    _use_gettext = True
    logging.info("Supported locales: %s", sorted(_supported_locales))


class Locale(BabelCoreLocale):
    """Object representing a locale.

    After calling one of `load_translations` or `load_gettext_translations`,
    call `get` or `get_closest` to get a Locale object.
    """
    @classmethod
    def get_closest(cls, *locale_codes):
        """Returns the closest match for the given locale code."""
        for code in locale_codes:
            if not code:
                continue
            code = code.replace("-", "_")
            parts = code.split("_")
            if len(parts) > 2:
                continue
            elif len(parts) == 2:
                code = parts[0].lower() + "_" + parts[1].upper()
            if code in _supported_locales:
                return cls.get(code)
            if parts[0].lower() in _supported_locales:
                return cls.get(parts[0].lower())
        return cls.get(_default_locale)

    @classmethod
    def get(cls, code):
        """Returns the Locale for the given locale code.

        If it is not supported, we raise an exception.
        """
        if not hasattr(cls, "_cache"):
            cls._cache = {}
        if code not in cls._cache:
            assert code in _supported_locales
            translations = _translations.get(code, gettext.NullTranslations())
            locale = cls.parse(code)
            locale.translations = translations
            cls._cache[code] = locale
        return cls._cache[code]

    def translate(self, message, plural_message=None, count=None):
        if plural_message is not None:
            assert count is not None
            return self.translations.ungettext(message, plural_message, count)
        else:
            return self.translations.ugettext(message)

    def format_datetime(self, datetime=None, format='medium', tzinfo=None):
        """
        Return a date formatted according to the given pattern.

        :param datetime: the datetime object; if None, the current date and
                         time is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        :param tzinfo: the timezone to apply to the time for display

        >>> from datetime import datetime
        >>> locale = Locale.parse('pt_BR')
        >>> locale
        <Locale "pt_BR">
        >>> dt = datetime(2007, 04, 01, 15, 30)
        >>> locale.format_datetime(dt)
        u'01/04/2007 15:30:00'
        """
        return dates.format_datetime(datetime, format, tzinfo, self)

    def format_date(self, date=None, format='medium'):
        """
        Return a date formatted according to the locale.

        :param date: the date or datetime object; if None, the current date
                     is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        """
        return dates.format_date(date, format, self)

    def format_time(self, time=None, format='medium', tzinfo=None):
        """
        Return a time formatted according to the locale.

        :param time: the time or datetime object; if None, the current time
                     in UTC is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        :param tzinfo: the time-zone to apply to the time for display
        """
        return dates.format_time(time, format, tzinfo, self)

    def format_timedelta(self, delta, granularity='second',
                threshold=0.84999999999999998):
        """
        Return a time delta according to the rules of the given locale.

        :param delta: a timedelta object representing the time difference to
                      format, or the delta in seconds as an int value
        :param granularity: determines the smallest unit that should be
                            displayed, the value can be one of "year",
                            "month", "week", "day", "hour", "minute" or
                            "second"
        :param threshold: factor that determines at which point the
                          presentation switches to the next higher unit
        """
        return dates.format_timedelta(delta, granularity, threshold, self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
