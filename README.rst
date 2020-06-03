==================================
sphinxcontrib-prettyspecialmethods
==================================

.. image:: https://travis-ci.org/sphinx-contrib/prettyspecialmethods.svg?branch=master
    :target: https://travis-ci.org/sphinx-contrib/prettyspecialmethods

Shows special methods as the python syntax that invokes them

Overview
--------

This module renders docs like

.. code-block:: rst

    .. method:: __add__(other)
        Docstring


as

self + other
    Docstring


After installing this module, add the following to your `conf.py` to enable it

.. code-block:: python

    extensions = [
        ...  # your other extensions
        'sphinxcontrib.prettyspecialmethods',
    ]


Links
-----

- Source: https://github.com/sphinx-contrib/prettyspecialmethods
- Bugs: https://github.com/sphinx-contrib/prettyspecialmethods/issues
