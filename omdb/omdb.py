''' OMDB API python wrapper library '''
from math import ceil

import requests

from .exceptions import OMDBException, OMDBNoResults, OMDBLimitReached, OMDBTooManyResults, OMDBInvalidAPIKey
from .utilities import camelcase_to_snake_case, range_inclusive, to_int


class OMDB(object):
    ''' The OMDB API wrapper instance

        Args:
            api_key (str): The API Key to use for the requests
            timeout (float): The timeout, in seconds
            strict (bool): To use strict error checking or not; strict (True) \
            will throw errors if the API returns an error code, non-strict will not
        Returns:
            OMDB: An OMDB API wrapper connection object
        Note:
            With `strict` disabled, it is up to the user to check for and handle errors '''

    __slots__ = ['_api_url', '_timeout', '_api_key', '_session', '_strict']

    def __init__(self, api_key, timeout=5, strict=True):
        ''' the init object '''
        self._api_url = 'https://www.omdbapi.com/'
        self._timeout = None
        self.timeout = timeout
        self._api_key = None
        self.api_key = api_key
        self._strict = None
        self.strict = strict
        self._session = requests.Session()

    def close(self):
        ''' Close the requests connection if necessary '''
        if self._session:
            self._session.close()
            self._session = None

    @property
    def api_key(self):
        ''' str: The API Key to use to connect to the OMDB API '''
        return self._api_key

    @api_key.setter
    def api_key(self, val):
        ''' set the API Key '''
        if isinstance(val, str):
            self._api_key = val
        else:
            raise OMDBInvalidAPIKey(val)

    @property
    def timeout(self):
        ''' float: The timeout parameter to pass to requests for how long to wait '''
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        ''' set the timeout property '''
        try:
            self._timeout = float(val)
        except ValueError:
            msg = "OMDB Timeout must be a float or convertable to float! {} provided".format(val)
            raise ValueError(msg)

    @property
    def strict(self):
        ''' bool: Whether to throw or swallow errors; True will throw exceptions '''
        return self._strict

    @strict.setter
    def strict(self, val):
        ''' set the strict property '''
        self._strict = bool(val)

    def search(self, title, pull_all_results=True, page=1, **kwargs):
        ''' Perform a search based on title

            Args:
                title (str): The query string to lookup
                page (int): The page of results to return
                pull_all_results (bool): True to return all results; False to pull page only
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Note:
                If `pull_all_results` is `True` then page is ignored '''
        params = {
            's': title,
            'page': 1,  # set to the default...
            'apikey': self.api_key
        }

        if not pull_all_results:
            params['page'] = page  # we are going to set it so that we can pull everything!

        params.update(kwargs)

        results = self._get_response(params)

        total_results = int(results.get('total_results', 0))
        if not pull_all_results or total_results <= 10:  # 10 is the max that it will ever return
            return results

        if 'search' not in results:
            results['search'] = list()  # defensive

        max_i = ceil(total_results/10)
        for i in range_inclusive(2, max_i):
            params.update({'page': i})
            data = self._get_response(params)
            results['search'].extend(data.get('search', list()))

        return results

    def get(self, *, title=None, imdbid=None, **kwargs):
        ''' Retrieve a specific movie, series, or episode

            Args:
                title (str): The title of the movie, series, or episode to return
                imdbid (str): The IMDB Id to use to pull the result
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Raises:
                OMDBException: Raised when both title or imdbid is not provided
            Note:
                Either `title` or `imdbid` is required '''
        params = {
            'apikey': self.api_key
        }
        if imdbid:
            params['i'] = imdbid
        elif title:
            params['t'] = title
        else:
            raise OMDBException("Either title or imdbid is required!")

        params.update(kwargs)

        return self._get_response(params)

    def search_movie(self, title, pull_all_results=True, page=1, **kwargs):
        ''' Search for a movie by title

            Args:
                title (str): The name, or part of a name, of the movie to look up
                pull_all_results (bool): True to return all results; False to pull page only
                page (int): The page of results to return
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results '''
        params = {'type': 'movie'}
        params.update(kwargs)
        return self.search(title, pull_all_results, page, **params)

    def search_series(self, title, pull_all_results=True, page=1, **kwargs):
        ''' Search for a TV series by title

            Args:
                title (str): The name, or part of a name, of the TV series to look up
                pull_all_results (bool): True to return all results; False to pull page only
                page (int): The page of results to return
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results '''
        params = {'type': 'series'}
        params.update(kwargs)
        return self.search(title, pull_all_results, page, **params)

    def get_movie(self, *, title=None, imdbid=None, **kwargs):
        ''' Retrieve a movie by title or IMDB id

            Args:
                title (str): The name of the movie to retrieve
                imdbid (str): The IMDB id of the movie to retrieve
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Note:
                Either `title` or `imdbid` is required '''
        params = {'type': 'movie'}
        params.update(kwargs)
        return self.get(title=title, imdbid=imdbid, **params)

    def get_series(self, *, title=None, imdbid=None, pull_episodes=False, **kwargs):
        ''' Retrieve a TV series information by title or IMDB id

            Args:
                title (str): The name of the movie to retrieve
                imdbid (str): The IMDB id of the movie to retrieve
                pull_episodes (bool): `True` to pull the episodes
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Note:
                Either `title` or `imdbid` is required '''
        params = {'type': 'series'}
        params.update(kwargs)
        res = self.get(title=title, imdbid=imdbid, **params)
        num_seasons = 0
        if pull_episodes:
            num_seasons = to_int(res.get('total_seasons', 0))
            res['seasons'] = dict()

        for i in range(num_seasons):
            season_num = i + 1
            season = self.get_episodes(title, imdbid, season=season_num)
            res['seasons'][season_num] = season

        return res

    def get_episode(self, *, title=None, imdbid=None, season=1, episode=1, **kwargs):
        ''' Retrieve a TV series episode by title or IMDB id and season and episode number

            Args:
                title (str): The name of the movie to retrieve
                imdbid (str): The IMDB id of the movie to retrieve
                season (int): The season number of the episode to retrieve
                episode (int): The episode number (based on season) of the episode to retrieve
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Note:
                Either `title` or `imdbid` is required '''
        params = {'type': 'episode'}
        if season:
            params['Season'] = season
        if episode:
            params['Episode'] = episode
        params.update(kwargs)
        return self.get(title=title, imdbid=imdbid, **params)

    def get_episodes(self, *, title=None, imdbid=None, season=1, **kwargs):
        ''' Retrieve all episodes of a TV series by season number

            Args:
                title (str): The name of the movie to retrieve
                imdbid (str): The IMDB id of the movie to retrieve
                season (int): The season number of the episode to retrieve
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Note:
                Either `title` or `imdbid` is required '''
        return self.get_episode(title=title, imdbid=imdbid, season=season, episode=None, **kwargs)

    def _get_response(self, kwargs):
        ''' wrapper for the `requests` library call '''
        # response = self._session.get(self._api_url, params=kwargs, timeout=self._timeout).json(encoding='utf8')
        response = self._session.get(self._api_url, params=kwargs, timeout=self._timeout).json()
        return self.__format_results(response, kwargs)

    def __format_results(self, res, params):
        ''' format the results into non-camelcase dictionaries '''
        if not isinstance(res, dict):
            raise TypeError('Expecting dict type, recieved {}'.format(type(res)))

        keys = sorted([x for x in res.keys()])
        for key in keys:
            val = res.pop(key)
            if isinstance(val, dict):
                val = self.__format_results(val, params)
            if isinstance(val, list):
                tmp = list()
                for _, itm in enumerate(val):
                    if isinstance(itm, dict):
                        tmp.append(self.__format_results(itm, params))
                    else:
                        tmp.append(itm)
                val = tmp

            # convert camel case to lowercase
            res[camelcase_to_snake_case(key)] = val

        # NOTE: I dislike having to use string comparisons to check for specific error conditions
        if self.strict and 'response' in res and res['response'] == 'False':
            err = res.get('error', '').lower()
            if err == 'too many results.':
                raise OMDBTooManyResults(res['error'], params)
            elif err == 'movie not found!':
                raise OMDBNoResults(res['error'], params)
            elif err == 'request limit reached!':
                raise OMDBLimitReached(self.api_key)
            elif err == 'invalid api key!':
                raise OMDBInvalidAPIKey(self.api_key)
            raise OMDBException('An unknown exception was returned: {}'.format(err))

        return res
