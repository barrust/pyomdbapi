import requests

from .exceptions import OMDBException, OMDBNoResults, OMDBLimitReached


class OMDB(object):

    def __init__(self, api_key, timeout=5):
        self._api_url = 'https://www.omdbapi.com/'
        self._timeout = timeout
        self._api_key = api_key
        self._session = requests.Session()

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def search(self, title, **params):
        prms = {
            's': title,
            'apikey': self._api_key
        }
        prms.update(params)

        data = self._get_response(prms)
        return self.__format_results(data, prms)

    def get(self, title=None, imdbid=None, **params):
        prms = {
            'apikey': self._api_key
        }
        if imdbid:
            prms['i'] = imdbid
        if title:
            prms['t'] = title
        else:
            raise OMDBException("Either title or imdbid is required!")

        prms.update(params)

        data = self._get_response(prms)
        return self.__format_results(data, prms)

    def search_movie(self, title, **params):
        prms = {'type': 'movie'}
        prms.update(params)
        data = self.search(title, **prms)
        return self.__format_results(data, prms)

    def search_series(self, title, **params):
        prms = {'type': 'series'}
        prms.update(params)
        return self.search(title, **prms)

    # def search_episode(self, title, **params):
    #     prms = {'type': 'episode'}
    #     prms.update(params)
    #     return self.search(title, **prms)

    def get_movie(self, title=None, imdbid=None, **params):
        prms = {'type': 'movie'}
        prms.update(params)
        return self.get(title, imdbid, **prms)

    def get_series(self, title=None, imdbid=None, **params):
        prms = {'type': 'series'}
        prms.update(params)
        return self.get(title, imdbid, **prms)

    def get_episode(self, title=None, imdbid=None, season=1, episode=1, **params):
        prms = {'type': 'episode'}
        if season:
            prms['Season'] = season
        if episode:
            prms['Episode'] = episode
        prms.update(params)
        return self.get(title, imdbid, **prms)

    def get_episodes(self, title=None, imdbid=None, season=1, **params):
        return self.get_episode(title, imdbid, season, None, **params)

    def _get_response(self, params):
        return self._session.get(self._api_url, params=params,
                                 timeout=self._timeout).json(encoding='utf8')

    def __format_results(self, res, params):
        if not isinstance(res, dict):
            raise TypeError('Expecting dict type, recieved type(res)')

        keys = res.keys()
        for key in keys:
            val = res.pop(key)
            if isinstance(val, dict):
                val = self.format_results(val, params)
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
