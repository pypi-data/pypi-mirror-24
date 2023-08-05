rockfinder
==========

[![Documentation Status](https://readthedocs.org/projects/rockfinder/badge/)](http://rockfinder.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.rawgit.com/thespacedoctor/rockfinder/master/coverage.svg)](https://cdn.rawgit.com/thespacedoctor/rockfinder/master/htmlcov/index.html)

*A python package and command-line tools for A python package and command-line suite to generate solar-system body ephemerides and to determine if specific transient dections are in fact known asteroids*.

Command-Line Usage
==================

Installation
============

The easiest way to install rockfinder is to use `pip`:

``` sourceCode
pip install rockfinder
```

Or you can clone the [github repo](https://github.com/thespacedoctor/rockfinder) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/rockfinder.git
cd rockfinder
python setup.py install
```

To upgrade to the latest version of rockfinder use the command:

``` sourceCode
pip install rockfinder --upgrade
```

Documentation
=============

Documentation for rockfinder is hosted by [Read the Docs](http://rockfinder.readthedocs.org/en/stable/) (last [stable version](http://rockfinder.readthedocs.org/en/stable/) and [latest version](http://rockfinder.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

Before you begin using rockfinder you will need to populate some custom settings within the rockfinder settings file.

To setup the default settings file at `~/.config/rockfinder/rockfinder.yaml` run the command:

``` sourceCode
rockfinder init
```

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an `XXX` placeholder).
