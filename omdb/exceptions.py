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


class OMDBInvalidAPIKey(OMDBException):
    ''' Invalide API Key provided

        Args:
            api_key (str): The API Key used that generated the exception
    '''
    def __init__(self, api_key):
        self._api_key = api_key
        super(OMDBInvalidAPIKey, self).__init__('Invalid API Key ({}) provided'.format(self.api_key))

    @property
    def api_key(self):
        ''' str: The exception message '''
        return self._api_key


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
        super(OMDBNoResults, self).__init__('message: {}\tparams: {}'.format(self.error, self.params))

    @property
    def error(self):
        ''' str: The OMDB API exception message '''
        return self._message

    @property
    def params(self):
        ''' dict: The parameters used when the exception was raised '''
        return self._params


class OMDBTooManyResults(OMDBException):
    ''' Too many results would be returned (per the OMDB API)

        Args:
            error (str): The error message returned by the OMDB API service
            params (dict): The parameters used when the exception was raised
    '''
    def __init__(self, error, params):
        ''' init '''
        self._params = params
        self._error = error
        super(OMDBTooManyResults, self).__init__('message: {}\tparams: {}'.format(self.error, self.params))

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
        super(OMDBLimitReached, self).__init__('Limit reached for API Key: {}'.format(self.api_key))

    @property
    def api_key(self):
        ''' str: The OMDB API API key used '''
        return self._api_key
