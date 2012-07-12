.. Tornado-Babel documentation master file, created by
   sphinx-quickstart on Thu Jul 12 16:34:09 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tornado-Babel
=============

.. py:currentmodule:: tornadobabel

Tornado-Babel adds i18n and l10n support to `tornado`_ with the help of
`babel`_ and `speaklater`_. It has builtin support for date formatting as
well as a very simple and friendly interface to :mod:`gettext`
translations.

Torando comes bundled with pretty basic locale support basic and does 
not offer support for merging translation catalogs and several other 
features most multi language applications require. The module also adds
more date and number formatting helpers.

Tornado-Babel also includes a plugin for Babel to extract translatable
strings from tornado templates.


Installation
------------

Install the extension with one of the following commands:

.. code-block:: sh

    $ easy_install Tornado-Babel

or alternatively if you have pip installed:

.. code-block:: sh

    $ pip install Tornado-Babel


Date Formatting
---------------

To format dates you can use the 
:meth:`~locale.Locale.format_datetime`. 
Here are some examples::

    >>> from datetime import datetime
    >>> from tornadobabel.locale import Locale
    >>> locale = Locale.parse('pt_BR')
    >>> locale
    <Locale "pt_BR">
    >>> dt = datetime(2007, 04, 01, 15, 30)
    >>> locale.format_datetime(dt)
    u'01/04/2007 15:30:00'

With a  different locale::

    >>> locale = Locale.parse('en_US')
    >>> locale
    <Locale "en_US">
    >>> dt = datetime(2007, 04, 01, 15, 30)
    >>> locale.format_datetime(dt)
    u'Apr 1, 2007 3:30:00 PM'

For more format examples head over to the `babel`_ documentation.


Using Translations
------------------

Making translatable applications
`````````````````````````````````
First you need to mark all the strings you want to translate in your
application. To use translation in your request handlers, you can use the
mixin :class:`~mixin.TornadoBabelMixin`: 


.. code-block:: python
    :emphasize-lines: 1
   
    from tornadobabel import locale

    class ProfileHandler(TornadoBabelMixin, ReuqestHandler):
        def get_user_locale(self):
            if self.current_user:
                return locale.get(self.current_user.locale)

            # Fallback to browser based locale detection
            return self.get_browser_locale()


The mixin adds a shortcut to :meth:`~locale.Locale.translate` 
as a property :meth:`~mixin.TornadoBabelMixin._`, which could 
be used like:

.. code-block:: python
    :emphasize-lines: 4,5 

    class HomePageHandler(TornadoBabelMixin, ReuqestHandler):

        def get(self):
            _ = self._
            return self.write(_("Hello"))


Extracting Translations
```````````````````````

After that, it's time to create a ``.pot`` file.  A ``.pot`` file contains 
all the strings and is the template for a ``.po`` file which contains the 
translated strings.  Babel can do all that for you.

First of all you have to get into the folder where you have your
application and create a mapping file.  For typical applications, this
is what you want in there:

.. sourcecode:: ini

    [python: **.py]
    [tornado: **/templates/**.html]

Save it as ``babel.cfg`` or something similar next to your application.
Then it's time to run the `pybabel` command that comes with Babel to
extract your strings:

.. code-block:: sh

    $ pybabel extract -F babel.cfg -o messages.pot .

If you are using the :func:`lazy_gettext` function you should tell pybabel
that it should also look for such function calls:

.. code-block:: sh

    $ pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

This will use the mapping from the ``babel.cfg`` file and store the
generated template in ``messages.pot``.  Now we can create the first
translation.  For example to translate to German use this command:

.. code-block:: sh

    $ pybabel init -i messages.pot -d translations -l de

``-d translations`` tells pybabel to store the translations in this
folder.  This is where Flask-Babel will look for translations.  Put it
next to your template folder.

Now edit the ``translations/de/LC_MESSAGES/messages.po`` file as needed.
Check out some gettext tutorials if you feel lost.

To compile the translations for use, ``pybabel`` helps again:

.. code-block:: sh

    $ pybabel compile -d translations

What if the strings change?  Create a new ``messages.pot`` like above and
then let ``pybabel`` merge the changes:

.. code-block:: sh

    $ pybabel update -i messages.pot -d translations

Afterwards some strings might be marked as fuzzy (where it tried to figure
out if a translation matched a changed key).  If you have fuzzy entries,
make sure to check them by hand and remove the fuzzy flag before
compiling.

Loading Translations
````````````````````

Now that you have a translatable application and translations, you can
load the translations of your application using 
:func:`~locale.load_gettext_translations`. The function takes two
arguments: `directory` which is the root path of the folder where
translations are stored and `domain` (which is used to match against
translation file names). In the above example, the directory would be the
absolute path of `translations` and the domain would be `messages`.

Babel also provides a powerful feature of merging translations from
multiple such directories and domains. This could be used when you use
third party modules which may have bundled translations along with it and
you want to use them with your application. An example of such a module is
`pycountry`_::

    >>> import pycountry
    >>> from tornadobabel.locale import load_gettext_translations
    >>> load_gettext_translations(pycountry.LOCALES_DIR, 'iso3166')

Now load your application translations::

    >>> load_gettext_translations('locales', 'messages')

Tornado-Babel will automatically merge both your translations::

    >>> pt_BR = locale.get("pt_BR")
    >>> pt_BR.translate("United States")
    u'Estados Unidos'


API Reference
-------------

Datetime Formatting Methods 
````````````````````````````
.. automethod:: tornadobabel.locale.Locale.format_datetime

.. automethod:: tornadobabel.locale.Locale.format_date

.. automethod:: tornadobabel.locale.Locale.format_time

.. automethod:: tornadobabel.locale.Locale.format_timedelta

Mixin Utilities for Tornado
````````````````````````````

.. autoclass:: tornadobabel.mixin.TornadoBabelMixin
    :members:

Low level API for message extraction
````````````````````````````````````

.. automodule:: tornadobabel.extract
   :members: GETTEXT_FUNCTIONS, DummyTemplate, walk, extract_from_node, extract_tornado
    

.. _babel: http://babel.edgewall.org/
.. _speaklater: http://pypi.python.org/pypi/speaklater
.. _tornado: http://www.tornadoweb.org/documentation
