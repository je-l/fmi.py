.. image:: https://img.shields.io/pypi/pyversions/fmi.py.svg?style=flat-square
    :target: https://pypi.org/project/fmi.py/

.. image:: https://img.shields.io/travis/je-l/fmi.py.svg?style=flat-square
    :target: https://travis-ci.org/je-l/fmi.py


Fmi.py is a library providing simple interface for interacting with FMI weather
and forecast API.

Some differences to other similar projects:

* Asyncio
* No scraping

Installation
------------

.. code:: bash

    pip install fmi.py

Documentation
-------------

https://fmipy.readthedocs.io/

Development
-----------

pip-tools_ is used for managing dependencies. First create virtualenv with
supported python version, and then:

.. code:: bash

    pip install pip-tools
    pip-sync

Alternatively use docker:

.. code:: bash

    docker build -t fmi.py
    docker run -it fmi.py


.. _pip-tools: https://github.com/jazzband/pip-tools
