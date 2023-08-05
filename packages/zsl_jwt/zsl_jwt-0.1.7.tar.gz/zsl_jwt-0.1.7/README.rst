========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/zsl_jwt/badge/?style=flat
    :target: https://readthedocs.org/projects/zsl_jwt
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/AtteqCom/zsl_jwt.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/AtteqCom/zsl_jwt

.. |coveralls| image:: https://coveralls.io/repos/AtteqCom/zsl_jwt/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/AtteqCom/zsl_jwt

.. |codecov| image:: https://codecov.io/github/AtteqCom/zsl_jwt/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/AtteqCom/zsl_jwt

.. |version| image:: https://img.shields.io/pypi/v/zsl-jwt.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/zsl-jwt

.. |commits-since| image:: https://img.shields.io/github/commits-since/AtteqCom/zsl_jwt/v0.1.7.svg
    :alt: Commits since latest release
    :target: https://github.com/AtteqCom/zsl_jwt/compare/v0.1.7...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/zsl-jwt.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/zsl-jwt

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/zsl-jwt.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/zsl-jwt

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/zsl-jwt.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/zsl-jwt


.. end-badges

JWT implementation for ZSL framework. This modules adds security
possibilities to ZSL.

* Free software: BSD license

Installation
============

Just add `zsl_jwt` to your requirements or use
::

    pip install zsl-jwt


Usage
=====

Add `zsl_jwt.module.JWTModule` to the modules in your `IoCContainer`
and provide a `zsl_jwt.configuration.JWTConfiguration` in your
configuration under `JWT` variable.

Documentation
=============

See more in https://zsl_jwt.readthedocs.io/

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
