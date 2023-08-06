=================
 ``zope.minmax``
=================

.. image:: https://img.shields.io/pypi/v/zope.minmax.svg
        :target: https://pypi.python.org/pypi/zope.minmax/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.minmax.svg
        :target: https://pypi.org/project/zope.minmax/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.minmax.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.minmax

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.minmax/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.minmax?branch=master

.. image:: https://readthedocs.org/projects/zopeminmax/badge/?version=latest
        :target: https://zopeminmax.readthedocs.io/en/latest/
        :alt: Documentation Status

This package provides support for homogeneous values favoring maximum
or minimum (e.g., numbers) for ZODB conflict resolution.

See https://zopeminmax.readthedocs.io for a detailed description.


=========
 Changes
=========

2.2.0 (2017-08-14)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.

- Bring unit test coverage to 100% (including branches).

- Convert doctests to Sphinx documentation, including building docs
  and running doctest snippets under ``tox``.

- Host documentation at https://zopeminmax.readthedocs.io

2.1.0 (2014-12-27)
==================

- Add support for PyPy3.

- Add support Python 3.4.


2.0.0 (2013-02-19)
==================

- Add support for Python 3.3 and PyPy.

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.


1.1.2 (2009-09-24)
==================

- Use the standard Python doctest module instead of the deprecated
  zope.testing.doctest.


1.1.1 (2009-09-09)
==================

- Fix homepage link and mailing list address.


1.1 (2007-10-02)
================

- Refactor package setup.


1.0 (2007-09-28)
================

- No further changes since 1.0b2


1.0b2 (2007-07-09)
==================

- Remove ``_p_independent`` method from ``AbstractValue`` class.


1.0b1 (2007-07-03)
==================

- Initial release.


