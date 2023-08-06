================
 ``zope.login``
================

.. image:: https://img.shields.io/pypi/v/zope.login.svg
        :target: https://pypi.python.org/pypi/zope.login/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.login.svg
        :target: https://pypi.org/project/zope.login/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.login.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.login

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.login/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.login?branch=master

.. image:: https://readthedocs.org/projects/zopelogin/badge/?version=latest
        :target: https://zopelogin.readthedocs.io/en/latest/
        :alt: Documentation Status

This package provides login helpers for `zope.publisher
<https://zopepublisher.readethedocs.io/>`_ based on the concepts of
`zope.authentication <https://zopeauthentication.readthedocs.io>`_.
This includes support for HTTP password logins and FTP logins.

Documentation is hosted at https://zopelogin.readthedocs.io


=========
 Changes
=========

2.1.0 (2017-09-01)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.

- Host documentation at https://zopelogin.readthedocs.io/

2.0.0 (2014-12-24)
==================

- Add support for PyPy and PyPy3.

- Add support for Python 3.4.

- Add support for testing on Travis.

- Add support for Python 3.3.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


1.0.0 (2009-12-31)
==================

- Extracted BasicAuthAdapter and FTPAuth adapters from zope.publisher. They
  should have never gone into that package in the first place.


