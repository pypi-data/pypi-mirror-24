========
Overview
========



embed.ly cards for Pelican blog, version 0.2.0

* Free software: BSD license

Installation
============

::

    pip install pelican-embedly

Documentation
=============

https://python-pelican_embedly.readthedocs.io/

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

0.1.0 (2017-07-23)
------------------

* First release on PyPI.


