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

.. code-block:: bash 
   
    
    Usage:
        rockfinder where [-e] [csv|md|rst|json|yaml] <objectId> <mjd>...
    
        csv                   output results in csv format
        md                    output results as a markdown table
        rst                   output results as a restructured text table
        json                  output results in json format
        yaml                  output results in yaml format
        -e, --extra           return extra ephemeris info (verbose)
        -h, --help            show this help message
    

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

.. Before you begin using rockfinder you will need to populate some custom settings within the rockfinder settings file.

.. To setup the default settings file at ``~/.config/rockfinder/rockfinder.yaml`` run the command:

.. .. code-block:: bash 
    
..     rockfinder init

.. This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an ``XXX`` placeholder). 

Let's say we want to generate an ephemeris for Ceres. We can either identify Ceres with its human-friendly name, its MPC number (`1`) or its MPC packed format (`00001`). I can grab an ephemeris from the JPL-Horizons for MJD=57967.564 with either of the following commands:

.. code-block:: bash 
    
    rockfinder where 1 57967.546
    rockfinder where ceres 57967.546
    rockfinder where 00001 57967.546

This returns the ephemeris in a neatly formatted table:

.. code-block:: text 
    
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+
    | mjd         | ra_deg    | dec_deg  | ra_3sig_error  | dec_3sig_error  | ra_arcsec_per_hour  | dec_arcsec_per_hour  | apparent_mag  | heliocentric_distance  | observer_distance  | phase_angle  |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+
    | 57967.5460  | 100.2386  | 24.2143  | 0.0000         | 0.0000          | 61.8963             | 0.8853               | 8.9100        | 2.6668                 | 3.4864             | 11.2662      |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+ 

To make the results returned from Horizons a little more verbose, use the `-e` flag:

.. code-block:: bash 
    
    rockfinder where -e ceres 57967.546

.. code-block:: text 

    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+----------------------+--------------------+------------------+--------------+---------------------+---------------------+-----------------------+-----------------------+----------------------------------+----------------------------+---------------------------+
    | mjd         | ra_deg    | dec_deg  | ra_3sig_error  | dec_3sig_error  | ra_arcsec_per_hour  | dec_arcsec_per_hour  | apparent_mag  | heliocentric_distance  | heliocentric_motion  | observer_distance  | observer_motion  | phase_angle  | true_anomaly_angle  | surface_brightness  | sun_obs_target_angle  | sun_target_obs_angle  | apparent_motion_relative_to_sun  | phase_angle_bisector_long  | phase_angle_bisector_lat  |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+----------------------+--------------------+------------------+--------------+---------------------+---------------------+-----------------------+-----------------------+----------------------------------+----------------------------+---------------------------+
    | 57967.5460  | 100.2386  | 24.2143  | 0.0000         | 0.0000          | 61.8963             | 0.8853               | 8.9100        | 2.6668                 | -1.2317              | 3.4864             | -13.2972         | 11.2662      | 294.8837            | 6.5600              | 30.8803               | 11.2614               | L                                | 93.6995                    | 1.2823                    |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+----------------------+--------------------+------------------+--------------+---------------------+---------------------+-----------------------+-----------------------+----------------------------------+----------------------------+---------------------------+

Returning a multi-epoch ephemeris
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To return an ephemeris covering multiple epoch, simply append extra MJD values to the command:

.. code-block:: bash 
    
    rockfinder where ceres 57967.546 57970.146 57975.683 57982.256 57994.547

.. code-block:: text 

    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+
    | mjd         | ra_deg    | dec_deg  | ra_3sig_error  | dec_3sig_error  | ra_arcsec_per_hour  | dec_arcsec_per_hour  | apparent_mag  | heliocentric_distance  | observer_distance  | phase_angle  |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+
    | 57967.5460  | 100.2386  | 24.2143  | 0.0000         | 0.0000          | 61.8963             | 0.8853               | 8.9100        | 2.6668                 | 3.4864             | 11.2662      |
    | 57970.1460  | 101.4080  | 24.2238  | 0.0000         | 0.0000          | 61.6860             | -0.0088              | 8.9100        | 2.6649                 | 3.4666             | 11.7406      |
    | 57975.6830  | 103.8887  | 24.2210  | 0.0000         | 0.0000          | 60.6418             | -0.3915              | 8.9200        | 2.6610                 | 3.4221             | 12.7383      |
    | 57982.2560  | 106.8029  | 24.1784  | 0.0000         | 0.0000          | 60.9023             | -1.6280              | 8.9200        | 2.6565                 | 3.3653             | 13.8893      |
    | 57994.5470  | 112.1475  | 24.0019  | 0.0000         | 0.0000          | 58.6741             | -2.6660              | 8.9100        | 2.6481                 | 3.2476             | 15.9324      |
    +-------------+-----------+----------+----------------+-----------------+---------------------+----------------------+---------------+------------------------+--------------------+--------------+

Changing the output format
~~~~~~~~~~~~~~~~~~~~~~~~~~

The command-line version of rockfinder has the ability to output the ephemeris results in various formats (csv, json, markdown table, restructured text table, yaml, ascii table). State an output format to render the results:

.. code-block:: bash 
    
    rockfinder where -e json ceres 57967.546

.. code-block:: text 

    [
        {
            "apparent_mag": 8.91,
            "apparent_motion_relative_to_sun": "L",
            "dec_3sig_error": 0.0,
            "dec_arcsec_per_hour": 0.885313,
            "dec_deg": 24.2142655,
            "heliocentric_distance": 2.666789121428,
            "heliocentric_motion": -1.231677,
            "mjd": 57967.54600000009,
            "observer_distance": 3.48635600851733,
            "observer_motion": -13.2971761,
            "phase_angle": 11.2662,
            "phase_angle_bisector_lat": 1.2823,
            "phase_angle_bisector_long": 93.6995,
            "ra_3sig_error": 0.0,
            "ra_arcsec_per_hour": 61.89635,
            "ra_deg": 100.2386357,
            "sun_obs_target_angle": 30.8803,
            "sun_target_obs_angle": 11.2614,
            "surface_brightness": 6.56,
            "true_anomaly_angle": 294.8837
        }
    ]



