pyramid_force_https
===================

------------
Introduction
------------

pyramid_force_https is a `tween <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#registering-tweens>`_ for `Pyramid <http://www.trypyramid.com/>`_ to redirect all HTTP requests to HTTPS.

------------
Installation
------------

Just do

``pip install pyramid_force_https``

or

``easy_install pyramid_force_https``

-------------
Compatibility
-------------

pyramid_force_https runs with pyramid>=1.7 and python>=2.7 and python>=3.5.
Other versions might also work.

-------------
Documentation
-------------

Usage example::

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_force_https')
        return config.make_wsgi_app()

See tests for more examples.

If you use structlog, add the following configuration setting to your INI file to enable structlog-like logging::

    pyramid_force_https.structlog = true


Releasing
---------

#. Update CHANGES.rst.
#. Update setup.py version.
#. Run ``bin/longtest``.
#. Run ``bin/mkrelease -d pypi``.
