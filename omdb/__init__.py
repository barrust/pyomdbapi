''' the omdb module '''

from .omdb import OMDB
from .exceptions import OMDBException, OMDBNoResults, OMDBLimitReached, OMDBTooManyResults

__author__ = 'Tyler Barrus'
__maintainer__ = 'Tyler Barrus'
__email__ = 'barrust@gmail.com'
__license__ = 'MIT'
__version__ = '0.2.0'
__url__ = 'https://github.com/barrust/pyomdbapi'
__bugtrack_url__ = '{0}/issues'.format(__url__)
__all__ = ['OMDB', 'OMDBException', 'OMDBNoResults', 'OMDBLimitReached', 'OMDBTooManyResults']
