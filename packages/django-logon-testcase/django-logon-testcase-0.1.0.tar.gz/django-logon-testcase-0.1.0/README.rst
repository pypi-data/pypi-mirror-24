=============================
Django Logon TestCase
=============================

.. image:: https://badge.fury.io/py/django-logon-testcase.svg
    :target: https://badge.fury.io/py/django-logon-testcase

.. image:: https://travis-ci.org/petr.dlouhy/django-logon-testcase.svg?branch=master
    :target: https://travis-ci.org/petr.dlouhy/django-logon-testcase

.. image:: https://codecov.io/gh/petr.dlouhy/django-logon-testcase/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/petr.dlouhy/django-logon-testcase

Simple enhancement to the TestCase which creates user and loggs him in.

Documentation
-------------

The full documentation is at https://django-logon-testcase.readthedocs.io.

Quickstart
----------

Install Django Logon TestCase::

    pip install django-logon-testcase

Use it in your tests:

.. code-block:: python

    from django.test import TestCase

    from logon_testcase import LogonMixin

    class MyTestCase(LogonMixin, TestCase):
         ...

The logged user is available in `self.user` variable.

Features
--------

You can get your own user for the test by overriding `get_user` function:

.. code-block:: python

    class MyTestCase(LogonMixin):
         def get_user(self):
             return User.objects.create()


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
