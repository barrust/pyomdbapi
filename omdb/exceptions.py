""" Exceptions for the pyomdbapi project """


from typing import Dict


class OMDBException(Exception):
    """Base OMDB Exception

    Args:
        message (str): The exception message
    """

    def __init__(self, message: str):
        """init"""
        self._message = message
        super().__init__(self.message)

    @property
    def message(self) -> str:
        """str: The exception message"""
        return self._message


class OMDBInvalidAPIKey(OMDBException):
    """Invalide API Key provided

    Args:
        api_key (str): The API Key used that generated the exception
    """

    def __init__(self, api_key: str):
        self._api_key = api_key
        super().__init__(f"Invalid API Key ({self.api_key}) provided")

    @property
    def api_key(self) -> str:
        """str: The exception message"""
        return self._api_key


class OMDBNoResults(OMDBException):
    """A No results returned exception

    Args:
        error (str): The error message returned by the OMDB API service
        params (dict): The parameters used when the exception was raised
    """

    def __init__(self, error: str, params: Dict):
        """init"""
        self._params = params
        self._error = error
        super().__init__(f"\n\tmessage:\t{self.error}\n\tparams: \t{self.params}")

    @property
    def error(self) -> str:
        """str: The OMDB API exception message"""
        return self._error

    @property
    def params(self) -> Dict:
        """dict: The parameters used when the exception was raised"""
        return self._params


class OMDBTooManyResults(OMDBException):
    """Too many results would be returned (per the OMDB API)

    Args:
        error (str): The error message returned by the OMDB API service
        params (dict): The parameters used when the exception was raised
    """

    def __init__(self, error: str, params: Dict):
        """init"""
        self._params = params
        self._error = error
        super().__init__(f"\n\tmessage:\t{self.error}\n\tparams: \t{self.params}")

    @property
    def error(self) -> str:
        """str: The OMDB API exception message"""
        return self._error

    @property
    def params(self) -> Dict:
        """dict: The parameters used when the exception was raised"""
        return self._params


class OMDBLimitReached(OMDBException):
    """Reached the limit of requests for the user - API Key combination

    Args:
        api_key (str): The API Key used when connecting to the OMDB API service
    """

    def __init__(self, api_key: str):
        """init"""
        self._api_key = api_key
        super().__init__(f"Limit reached for API Key: {self.api_key}")

    @property
    def api_key(self) -> str:
        """str: The OMDB API API key used"""
        return self._api_key
