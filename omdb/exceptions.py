

class OMDBException(Exception):

    def __init__(self, message):
        self._message = message
        super(OMDBException, self).__init__(self.message)

    @property
    def message(self):
        ''' str: The MediaWiki exception message '''
        return self._message


class OMDBNoResults(OMDBException):

    def __init__(self, error, params):
        self._params = params
        self._error = error
        super(OMDBNoResults, self).__init__('message: {}\tparams: {}'.format(self._error, self._params))

    @property
    def error(self):
        ''' str: The MediaWiki exception message '''
        return self._message

    @property
    def params(self):
        ''' str: The MediaWiki exception message '''
        return self._params


class OMDBLimitReached(OMDBException):

    def __init__(self, api_key):
        self._api_key = api_key
        super(OMDBLimitReached, self).__init__('Limit reached for API Key: {}'.format(self._api_key))

    @property
    def api_key(self):
        ''' str: The MediaWiki exception message '''
        return self._api_key
