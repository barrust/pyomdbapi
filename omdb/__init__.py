""" the omdb module """

from omdb.exceptions import OMDBException, OMDBLimitReached, OMDBNoResults, OMDBTooManyResults
from omdb.omdb import OMDB

__author__ = "Tyler Barrus"
__maintainer__ = "Tyler Barrus"
__email__ = "barrust@gmail.com"
__license__ = "MIT"
__version__ = "0.2.2"
__url__ = "https://github.com/barrust/pyomdbapi"
__bugtrack_url__ = f"{__url__}/issues"
__all__ = [
    "OMDB",
    "OMDBException",
    "OMDBNoResults",
    "OMDBLimitReached",
    "OMDBTooManyResults",
]
