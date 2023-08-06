patatmo Python package 
======================

.. image:: https://gitlab.com/nobodyinperson/python3-patatmo/badges/master/build.svg
    :target: https://gitlab.com/nobodyinperson/python3-patatmo/commits/master

.. image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
    :target: https://nobodyinperson.gitlab.io/python3-patatmo/

.. image:: https://gitlab.com/nobodyinperson/python3-patatmo/badges/master/coverage.svg
    :target: https://nobodyinperson.gitlab.io/python3-patatmo/coverage-report

.. image:: https://badge.fury.io/py/patatmo.svg
   :target: https://badge.fury.io/py/patatmo

This package provides easy access to the `Netatmo <https://netatmo.com>`_
`API <https://dev.netatmo.com>`_.  It is **painless** as it completely and
intelligently hides the OAuth2 authentication from you. 

Disclaimer
++++++++++

    **This software to access the** `Netatmo Weather API <https://dev.netatmo.com/>`_ 
    **emerged as part of thesis and also out of private interest. 
    The author is not in any way affiliated with Netatmo (SAS).**

Capabilities
++++++++++++

Currently, the weather API's methods ``Getpublicdata``, ``Getstationsdata`` and
``Getmeasure`` are implemented.

Example usage
+++++++++++++

An example of obtaining all public station's data in the region of
Hamburg/Germany:

.. code:: python

    import patatmo

    # your netatmo connect developer credentials
    credentials = {
        "password":"5uP3rP45sW0rD",
        "username":"user.email@internet.com",
        "client_id":    "03012823b3fd2e420fbf980b",
        "client_secret":"YXNkZmFzZGYgamFzamYgbGFzIG"
    }

    # configure the authentication
    authentication = patatmo.api.authentication.Authentication(
        credentials=credentials,
        tmpfile = "temp_auth.json"
    )
    # providing a path to a tmpfile is optionally.
    # If you do so, the tokens are stored there for later reuse, 
    # e.g. next time you invoke this script.
    # This saves time because no new tokens have to be requested.
    # New tokens are then only requested if the old ones expire.

    # create a api client
    client = patatmo.api.client.NetatmoClient(authentication)
    
    # lat/lon outline of Hamburg/Germany
    hamburg_region = {
        "lat_ne" : 53.7499,
        "lat_sw" : 53.3809,
        "lon_ne" : 10.3471,
        "lon_sw" : 9.7085,
    }

    # issue the API request
    hamburg = client.Getpublicdata(region = hamburg_region)

    # convert the response to a pandas.DataFrame
    print(hamburg.dataframe())

.. code::

    output (excerpt):

         index   altitude  humidity                 id   latitude  longitude  \
    0        0  30.000000        84  70:ee:50:12:9a:b8  53.516950  10.155990   
    1        1  23.000000        83  70:ee:50:03:da:4c  53.523361  10.167193   
    2        2  23.000000        76  70:ee:50:01:47:34  53.510080  10.165600   
    3        3  15.000000        93  70:ee:50:03:bc:2c  53.530948  10.134062    
    ..     ...        ...       ...                ...        ...        ...   

         pressure  temperature       time_humidity       time_pressure  \
    0      1029.1          8.1 2017-02-16 10:59:31 2017-02-16 11:00:05   
    1      1026.7          8.3 2017-02-16 10:53:53 2017-02-16 10:54:01   
    2      1030.0          9.4 2017-02-16 10:53:06 2017-02-16 10:53:42   
    3      1026.8          8.0 2017-02-16 10:56:32 2017-02-16 10:56:54   
    ..        ...          ...                 ...                 ...   

           time_temperature       timezone  
    0   2017-02-16 10:59:31  Europe/Berlin  
    1   2017-02-16 10:53:53  Europe/Berlin  
    2   2017-02-16 10:53:06  Europe/Berlin  
    3   2017-02-16 10:56:32  Europe/Berlin   
    ..                  ...            ...  

    [708 rows x 12 columns]


Install
+++++++

This package is on `PyPi <https://pypi.python.org/pypi/patatmo>`_. To install `patatmo`,
run

.. code:: sh

    pip install --user patatmo

Documentation
+++++++++++++

You can find detailed documentation of this package 
`here on on Gitlab <https://nobodyinperson.gitlab.io/python3-patatmo/>`_.

Development
+++++++++++

The following might only be interesting for developers

Local installation
------------------

Install this module from the repository root via :code:`pip`:

.. code:: sh

    # local user library under ~/.local
    pip3 install --user .
    # in "editable" mode
    pip3 install --user -e .

Testing
-------

To be able to run *all* tests, you need to specify valid **credentials and a
device and model id** of your test station. You can do so either in the file
``tests/USER_DATA.json`` (e.g. copy the example file :code:`cp
tests/USER_DATA.json.example tests/USER_DATA.json` and adjust it) or via the
environment variables

.. code::

    NETATMO_CLIENT_ID
    NETATMO_CLIENT_SECRET
    NETATMO_USERNAME
    NETATMO_PASSWORD
    NETATMO_DEVICE_ID
    NETATMO_MODULE_ID

Otherwise, only the possible tests are run.

Then:

- ``make test`` to run all tests directly
- ``make testverbose`` to run all tests directly with verbose output
- ``make setup-test`` to run all tests via the ``./setup.py test`` mechanism
- ``make coverage`` to get a test coverage

Versioning
----------

- ``make increase-patch`` to increase the patch version number
- ``make increase-minor`` to increase the minor version number
- ``make increase-major`` to increase the major version number


