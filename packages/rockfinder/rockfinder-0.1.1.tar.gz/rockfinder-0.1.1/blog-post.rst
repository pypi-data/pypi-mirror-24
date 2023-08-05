rockfinder 
=========================

.. image:: https://readthedocs.org/projects/rockfinder/badge/
    :target: http://rockfinder.readthedocs.io/en/latest/?badge
    :alt: Documentation Status

.. image:: https://cdn.rawgit.com/thespacedoctor/rockfinder/master/coverage.svg
    :target: https://cdn.rawgit.com/thespacedoctor/rockfinder/master/htmlcov/index.html
    :alt: Coverage Status

*A python package and command-line tools for A python package and command-line suite to generate solar-system body ephemerides and to determine if specific transient dections are in fact known asteroids*.





Command-Line Usage
==================

.. todo::

    - add usage

Installation
============

The easiest way to install rockfinder is to use ``pip``:

.. code:: bash

    pip install rockfinder

Or you can clone the `github repo <https://github.com/thespacedoctor/rockfinder>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/rockfinder.git
    cd rockfinder
    python setup.py install

To upgrade to the latest version of rockfinder use the command:

.. code:: bash

    pip install rockfinder --upgrade


Documentation
=============

Documentation for rockfinder is hosted by `Read the Docs <http://rockfinder.readthedocs.org/en/stable/>`__ (last `stable version <http://rockfinder.readthedocs.org/en/stable/>`__ and `latest version <http://rockfinder.readthedocs.org/en/latest/>`__).

Command-Line Tutorial
=====================

Before you begin using rockfinder you will need to populate some custom settings within the rockfinder settings file.

To setup the default settings file at ``~/.config/rockfinder/rockfinder.yaml`` run the command:

.. code-block:: bash 
    
    rockfinder init

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an ``XXX`` placeholder). 

.. todo::

    - add tutorial

