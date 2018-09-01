pyomdbapi
===========

A simple OMDB API python wrapper

Installation
------------------

Pip Installation:

::

    $ pip install pyomdbapi

To install from source:

To install ``pyomdbapi``, simply clone the `repository on GitHub
<https://github.com/barrust/pyomdbapi>`__, then run from the folder:

::

    $ python setup.py install

`pyomdbapi` supports python versions 3.4 - 3.7


Quickstart
-------------------------------------------------------------------------------
To use ``pyomdbapi`` you will need to get an API Key from `the OMDBApi site
<http://www.omdbapi.com/>`__. There are several versions available
with the free version limiting to 1000 requests per day.


After installation, using ``pyomdbapi`` should be fairly straight forward:

.. code:: python

    from omdb import OMDB

    omdb = OMDB(YOUR_API_KEY)

    print(omdb.get_movie('despicable me'))
