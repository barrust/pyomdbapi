import requests

from .exceptions import OMDBException, OMDBNoResults, OMDBLimitReached


class OMDB(object):
    ''' The OMDB API wrapper instance

        Args:
            api_key (str): The API Key to use for the requests
            timeout (float): The timeout, in seconds
        Returns:
            OMDB: An OMDB API wrapper connection object '''

    def __init__(self, api_key, timeout=5):
        ''' the init object '''
        self._api_url = 'https://www.omdbapi.com/'
        self._timeout = timeout
        self._api_key = api_key
        self._session = requests.Session()

    def close(self):
        ''' Close the requests connection if necessary '''
        if self._session:
            self._session.close()
            self._session = None

    def search(self, title, **kwargs):
        ''' Perform a search based on title

            Args:
                title (str): The query string to lookup
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
        '''
        params = {
            's': title,
            'apikey': self._api_key
        }
        params.update(kwargs)

        data = self._get_response(params)
        return self.__format_results(data, params)

    def get(self, title=None, imdbid=None, **kwargs):
        '''
            Args:
                title (str): The title of the movie, series, or episode to return
                imdbid (str): The IMDB Id to use to pull the result
                kwargs (dict): the kwargs to add additional parameters to the API request
            Returns:
                dict: A dictionary of all the results
            Raises:
                OMDBException: Raised when both title or imdbid is not provided
            Note:
                Either `title` or `imdbid` is required
        '''
        params = {
            'apikey': self._api_key
        }
        if imdbid:
            params['i'] = imdbid
        if title:
            params['t'] = title
        else:
            raise OMDBException("Either title or imdbid is required!")

        params.update(kwargs)

        data = self._get_response(params)
        return self.__format_results(data, params)

    def search_movie(self, title, **kwargs):
        params = {'type': 'movie'}
        params.update(kwargs)
        data = self.search(title, **params)
        return self.__format_results(data, params)

    def search_series(self, title, **kwargs):
        params = {'type': 'series'}
        params.update(kwargs)
        return self.search(title, **params)

    # def search_episode(self, title, **params):
    #     params = {'type': 'episode'}
    #     params.update(params)
    #     return self.search(title, **params)

    def get_movie(self, title=None, imdbid=None, **kwargs):
        params = {'type': 'movie'}
        params.update(kwargs)
        return self.get(title, imdbid, **params)

    def get_series(self, title=None, imdbid=None, **kwargs):
        params = {'type': 'series'}
        params.update(kwargs)
        return self.get(title, imdbid, **params)

    def get_episode(self, title=None, imdbid=None, season=1, episode=1, **kwargs):
        params = {'type': 'episode'}
        if season:
            params['Season'] = season
        if episode:
            params['Episode'] = episode
        params.update(kwargs)
        return self.get(title, imdbid, **params)

    def get_episodes(self, title=None, imdbid=None, season=1, **kwargs):
        return self.get_episode(title, imdbid, season, None, **kwargs)

    def _get_response(self, kwargs):
        return self._session.get(self._api_url, params=kwargs,
                                 timeout=self._timeout).json(encoding='utf8')

    def __format_results(self, res, params):
        if not isinstance(res, dict):
            raise TypeError('Expecting dict type, recieved type(res)')

        keys = res.keys()
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
            res[key.lower()] = val

        if 'response' in res and res['response'] == 'False':
            raise OMDBNoResults(res['error'], params)

        return res
