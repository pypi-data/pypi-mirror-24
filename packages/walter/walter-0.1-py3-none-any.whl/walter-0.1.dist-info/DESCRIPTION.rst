Walter
======

.. warning::

    Walter is pre-release software. Expect the API to change without notice, and expect this documentation to have lots of sharp edges.

Walter is a configuration library, inspired by `python-decouple <https://pypi.python.org/pypi/python-decouple>`_, and intended to replace direct access to ``os.environ`` in Django ``settings.py`` files (although it is by no means Django-specific). It currently supports Python 3.5+.

It differs from other, similar libraries for two reasons:

- It will let you specify your configuration parameters in one place and have auto-generated Sphinx documentation, just like with Python code. (Work on this hasn't been started yet.)
- When your users try to start up your app with invalid configuration, the error message they get shows a list of **all of the errors** with every configuration parameter, not just the first one.

Installation
------------

::

    pip install walter

Usage
-----

::

    from walter.config import Config

    # Your configuration needs to be wrapped in a context manager,
    # so Walter can collect all the errors and display them at the end.
    with Config("SGC", "Dialer") as config:

        # Read a configuration value with config.get()
        SECRET_KEY = config.get('SECRET_KEY')

        # Convert the returned value to something other than a string with cast.
        DEBUG = config.get('DEBUG', cast=bool)

        # You can pass any function that takes a string to `cast`.
        # Here, we're using a third party function to parse a database URL
        # string into a Django-compatible dictionary.
        DATABASES = {
            'default': config.get('DATABASE_URL', cast=dj_database_url.parse),
        }

        # You can also make a parameter optional by giving it a default.
        RAVEN_DSN = config.get('RAVEN_DSN', default=None)

        # Last but not least, help_text is displayed in your Sphinx docs.
        SITE_NAME = config.get('SITE_NAME',
                               help_text="Displayed to users in the admin")

