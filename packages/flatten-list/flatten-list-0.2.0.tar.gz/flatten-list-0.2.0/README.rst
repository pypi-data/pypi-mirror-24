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

.. |docs| image:: https://readthedocs.org/projects/python-flatten-list/badge/?style=flat
    :target: https://readthedocs.org/projects/python-flatten-list
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/techdragon/python-flatten-list.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/techdragon/python-flatten-list

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/techdragon/python-flatten-list?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/techdragon/python-flatten-list

.. |requires| image:: https://requires.io/github/techdragon/python-flatten-list/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/techdragon/python-flatten-list/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/techdragon/python-flatten-list/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/techdragon/python-flatten-list

.. |landscape| image:: https://landscape.io/github/techdragon/python-flatten-list/master/landscape.svg?style=flat
    :target: https://landscape.io/github/techdragon/python-flatten-list/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/flatten-list.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/flatten-list

.. |commits-since| image:: https://img.shields.io/github/commits-since/techdragon/python-flatten-list/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/techdragon/python-flatten-list/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/flatten-list.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/flatten-list

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flatten-list.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/flatten-list

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flatten-list.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/flatten-list


.. end-badges

Flatten Irregular Nested Lists

* Free software: MIT license

Installation
============

::

    pip install flatten-list

Documentation
=============

https://python-flatten-list.readthedocs.io/

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
