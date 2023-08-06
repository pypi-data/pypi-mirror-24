==========================
 ``zope.processlifetime``
==========================


.. image:: https://img.shields.io/pypi/v/zope.processlifetime.svg
        :target: https://pypi.python.org/pypi/zope.processlifetime/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.processlifetime.svg
        :target: https://pypi.org/project/zope.processlifetime/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.processlifetime.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.processlifetime

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.processlifetime/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.processlifetime?branch=master

.. image:: https://readthedocs.org/projects/zopeprocesslifetime/badge/?version=latest
        :target: https://zopeprocesslifetime.readthedocs.io/en/latest/
        :alt: Documentation Status

This package provides interfaces / implementations for events relative
to the lifetime of a server process (startup, database opening, etc.)
These events are usually used with `zope.event
<http://zopeevent.readthedocs.io/en/latest/>`_.

Documentation is hosted at https://zopeprocesslifetime.readthedocs.io/en/latest/


=========
 Changes
=========

2.2.0 (2017-09-01)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6, 3.2 and 3.3.

- Host documentation at https://zopeprocesslifetime.readthedocs.io/en/latest/


2.1.0 (2014-12-27)
==================

- Add support for PyPy and PyPy3.

- Add support for Python 3.4.

- Add support for testing on Travis.


2.0.0 (2013-02-22)
==================

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Add support for Python 3.2 and 3.3

- Drop support for Python 2.4 and 2.5.



1.0 (2009-05-13)
================

- Split out event interfaces / implementations from ``zope.app.appsetup``
  version 3.10.2.


