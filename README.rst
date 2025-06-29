.. image:: https://results.pre-commit.ci/badge/github/sphinx-contrib/prettyspecialmethods/master.svg
    :target: https://results.pre-commit.ci/latest/github/sphinx-contrib/prettyspecialmethods/master
    :alt: pre-commit.ci status

.. image:: https://github.com/sphinx-contrib/prettyspecialmethods/actions/workflows/tests.yaml/badge.svg?branch=master
    :target: https://github.com/sphinx-contrib/prettyspecialmethods/actions/workflows/tests.yaml
    :alt: Github Actions status

==================================
sphinxcontrib-prettyspecialmethods
==================================

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


Installing
----------

Install this fork directly from github:

.. code-block:: sh

    pip install sphinxcontrib-prettyspecialmethods


After installing this module, add the following to your `conf.py` to enable it

.. code-block:: python

    extensions = [
        ...  # your other extensions
        'sphinxcontrib.prettyspecialmethods',
    ]
