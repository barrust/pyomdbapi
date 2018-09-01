.. _quickstart:

Quickstart
===============================================================================

``pyomdbapi`` is designed to be easy to use to retrieve metadata from the OMDB
API.


Installation
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

It is recommended to install using pip

Pip Installation:

::

    $ pip install pyomdbapi

To install from source:

To install ``pyomdbapi``, simply clone the `repository on GitHub
<https://github.com/barrust/pyomdbapi>`__, then run from the folder:

::

    $ python setup.py install

`pyomdbapi` supports python versions 3.4 - 3.7


Basic Usage
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To use ``pyomdbapi`` you will need to get an API key from the OMDB API site.
The keys are free to use so please `sign up<http://www.omdbapi.com/>`__!

Now that you have an API key and have activated it; we can begin using
pyomdbapi:

.. code:: python

    from omdb import OMDB

    API_KEY = <YOUR_API_KEY>
    omdb = OMDB(api_key=API_KEY)

    # pull our favorite movie information
    omdb.get_movie('So I married an Axe Murderer')

We can also pull series information and episode information:

.. code:: python

    from omdb import OMDB

    API_KEY = <YOUR_API_KEY>
    omdb = OMDB(api_key=API_KEY)

    # pull our favorite TV series information
    omdb.get_series('Psych')

    # get all the information about the second season
    omdb.get_episodes('Psych', season=2)

    # pull the information about season 4 episode 8
    omdb.get_episode('Psych', season=4, episode=8)


One can also search for movies or series by title:

.. code:: python

    from omdb import OMDB

    API_KEY = <YOUR_API_KEY>
    omdb = OMDB(api_key=API_KEY)

    # search for a movie "Aeon Flux"...
    omdb.search_movie('Aeon')

    # Search for the series "Parks and Recreation"
    omdb.search_series('recreation')
