''' Exceptions for the pyomdbapi project '''

class OMDBException(Exception):
    ''' Base OMDB Exception

        Args:
            message (str): The exception message
    '''
    def __init__(self, message):
        ''' init '''
        self._message = message
        super(OMDBException, self).__init__(self.message)

    @property
    def message(self):
        ''' str: The exception message '''
        return self._message


class OMDBNoResults(OMDBException):
    ''' A No results returned exception

        Args:
            error (str): The error message returned by the OMDB API service
            params (dict): The parameters used when the exception was raised
    '''
    def __init__(self, error, params):
        ''' init '''
        self._params = params
        self._error = error
        super(OMDBNoResults, self).__init__('message: {}\tparams: {}'.format(self._error, self._params))

    @property
    def error(self):
        ''' str: The OMDB API exception message '''
        return self._message

    @property
    def params(self):
        ''' dict: The parameters used when the exception was raised '''
        return self._params


class OMDBLimitReached(OMDBException):
    ''' Reached the limit of requests for the user - API Key combination

        Args:
            api_key (str): The API Key used when connecting to the OMDB API service
    '''
    def __init__(self, api_key):
        ''' init '''
        self._api_key = api_key
        super(OMDBLimitReached, self).__init__('Limit reached for API Key: {}'.format(self._api_key))

    @property
    def api_key(self):
        ''' str: The OMDB API API key used '''
        return self._api_key
