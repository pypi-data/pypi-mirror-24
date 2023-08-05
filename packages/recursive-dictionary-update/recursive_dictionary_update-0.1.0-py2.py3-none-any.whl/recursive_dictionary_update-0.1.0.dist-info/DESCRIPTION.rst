========
Overview
========



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


Changelog
=========

0.1.0 (2017-08-07)
------------------

* First release on PyPI.


