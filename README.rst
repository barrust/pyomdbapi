pyomdbapi
===========

A simple OMDB API python wrapper

.. image:: https://badge.fury.io/py/pyomdbapi.svg
    :target: https://badge.fury.io/py/pyomdbapi
    :alt: PyPy Version
.. image:: https://api.codacy.com/project/badge/Grade/e83dad34f35a44dea103100f23cd6310
    :target: https://www.codacy.com/app/barrust/pyomdbapi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=barrust/pyomdbapi&amp;utm_campaign=Badge_Grade
    :alt: Code Quality
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/
    :alt: License
.. image:: https://pepy.tech/badge/pyomdbapi
    :target: https://pepy.tech/project/pyomdbapi
    :alt: Downloads

Documenation
-------------------------------------------------------------------------------

Online documentation can be found on `readthedocs.org <https://pyomdbapi.readthedocs.io/en/latest/>`__.


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

`pyomdbapi` supports python versions 3.5 - 3.9


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
