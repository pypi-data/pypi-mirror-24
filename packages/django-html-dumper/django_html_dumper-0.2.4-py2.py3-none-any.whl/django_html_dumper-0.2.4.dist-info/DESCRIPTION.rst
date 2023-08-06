=============================
HTML dumper
=============================

.. image:: https://badge.fury.io/py/django-html-dumper.svg
    :target: https://badge.fury.io/py/django-html-dumper

.. image:: https://travis-ci.org/adrienbrunet/django-html-dumper.svg?branch=master
    :target: https://travis-ci.org/adrienbrunet/django-html-dumper

.. image:: https://codecov.io/gh/adrienbrunet/django-html-dumper/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/adrienbrunet/django-html-dumper

Dumps html pages and their corresponding assets into a tar file

Documentation
-------------

The full documentation is at https://django-html-dumper.readthedocs.io.

Quickstart
----------

Install HTML dumper::

    pip install django-html-dumper

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'html_dumper.apps.HtmlDumperConfig',
        ...
    )


Features
--------

* Add a django command `dump_html`

.. code-block::
    python manage.py dump_html [path/to/my/page1 my/page2] (default to ['/', ])


This will create a directory `HTML_OUTPUT` (name can be customized via `settings.SITE_OUTPUT_DIRECTORY`) which will contain :

* the content of the page under the given urls for all available languages
* the static folder (copied from the output of `collectstatic`, beware of all the admin assets...)

Running Tests
-------------

Does the code actually work?

.. code-block::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------


0.2.4 (2017-08-14)
++++++++++++++++++

* First usable (ish) version

0.1.0 (2017-08-14)
++++++++++++++++++

* First release on PyPI.


