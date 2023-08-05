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

.. |docs| image:: https://readthedocs.org/projects/python-techdragon/badge/?style=flat
    :target: https://readthedocs.org/projects/python-techdragon
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/techdragon/python-techdragon.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/techdragon/python-techdragon

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/techdragon/python-techdragon?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/techdragon/python-techdragon

.. |requires| image:: https://requires.io/github/techdragon/python-techdragon/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/techdragon/python-techdragon/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/techdragon/python-techdragon/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/techdragon/python-techdragon

.. |landscape| image:: https://landscape.io/github/techdragon/python-techdragon/master/landscape.svg?style=flat
    :target: https://landscape.io/github/techdragon/python-techdragon/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/techdragon.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/techdragon

.. |commits-since| image:: https://img.shields.io/github/commits-since/techdragon/python-techdragon/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/techdragon/python-techdragon/compare/v1.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/techdragon.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/techdragon

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/techdragon.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/techdragon

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/techdragon.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/techdragon


.. end-badges

My Contact Details

* Free software: MIT license

Installation
============

::

    pip install techdragon

Documentation
=============

https://python-techdragon.readthedocs.io/

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
