=======
pipstat
=======

.. image:: https://badge.fury.io/py/pipstat.png
    :target: http://badge.fury.io/py/pipstat
    :alt: Latest version

.. image:: https://travis-ci.org/sloria/pipstat.png?branch=master
    :target: https://travis-ci.org/sloria/pipstat
    :alt: Travis-CI

Get download statistics for PyPI packages from the command line.
::

    $ pipstat marshmallow
    Fetching statistics for 'marshmallow'. . .

    Download statistics for marshmallow
    ===================================
    Downloads by version
    0.1.0 [ 818 ] ********************************************************************
    0.2.0 [ 855 ] ***********************************************************************
    0.2.1 [ 806 ] *******************************************************************
    0.3.0 [ 760 ] ***************************************************************
    0.3.1 [ 695 ] *********************************************************
    0.4.0 [ 640 ] *****************************************************
    0.4.1 [ 695 ] *********************************************************
    0.5.0 [ 717 ] ***********************************************************
    0.5.1 [ 298 ] ************************

    Min downloads:      298 (0.5.1)
    Max downloads:      855 (0.2.0)
    Avg downloads:      698
    Total downloads:    6,284

Get it now
----------
::

    pip install pipstat


Requirements
------------

- Python >= 2.7 or >= 3.2

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/pipstat/blob/master/LICENSE>`_ file for more details.
