========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-recursive-dictionary-update/badge/?style=flat
    :target: https://readthedocs.org/projects/python-recursive-dictionary-update
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/techdragon/python-recursive-dictionary-update.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/techdragon/python-recursive-dictionary-update

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/techdragon/python-recursive-dictionary-update?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/techdragon/python-recursive-dictionary-update

.. |requires| image:: https://requires.io/github/techdragon/python-recursive-dictionary-update/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/techdragon/python-recursive-dictionary-update/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/techdragon/python-recursive-dictionary-update/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/techdragon/python-recursive-dictionary-update

.. |landscape| image:: https://landscape.io/github/techdragon/python-recursive-dictionary-update/master/landscape.svg?style=flat
    :target: https://landscape.io/github/techdragon/python-recursive-dictionary-update/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/recursive-dictionary-update.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/recursive-dictionary-update

.. |commits-since| image:: https://img.shields.io/github/commits-since/techdragon/python-recursive-dictionary-update/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/techdragon/python-recursive-dictionary-update/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/recursive-dictionary-update.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/recursive-dictionary-update

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/recursive-dictionary-update.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/recursive-dictionary-update

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/recursive-dictionary-update.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/recursive-dictionary-update


.. end-badges

Recursively Update a Dictionary

* Free software: MIT license

Installation
============

::

    pip install recursive-dictionary-update

Documentation
=============

https://python-recursive-dictionary-update.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
