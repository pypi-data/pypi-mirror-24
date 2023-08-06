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

Add HTML dumper's URL patterns:

.. code-block:: python

    from html_dumper import urls as html_dumper_urls


    urlpatterns = [
        ...
        url(r'^', include(html_dumper_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

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

0.1.0 (2017-08-14)
++++++++++++++++++

* First release on PyPI.


