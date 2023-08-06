"""
Base API
"""

import requests
from .exceptions import ParameterError, ApiKeyError, ApiFailure
from .utils import snake_to_camel_case

SYSTRANIO_URL = 'https://api-platform.systran.net'


class BaseAPI(object):
    """
    Base API class
    Subclasses all systran.io APIs (Translation, NLP, etc.)
    Calls are made with `requests`
    """
    key = ''

    def __init__(self, key):
        """
        Sets the API Key
        Get yours on https://systran.io
        """
        self.key = key

    def _set_attributes(self, **kwargs):
        """
        Loops through kwargs and tries to set attributes
        Attributes are API parameters so if it fails we raise an exception
        """
        for parameter, value in kwargs.items():
            try:
                getattr(self, parameter)  # trigger error
                setattr(self, parameter, value)
            except AttributeError:
                raise ParameterError(
                    'Invalid API parameter : {}'.format(parameter))

    @property
    def payload(self):
        """
        Like __dict__() but with camelCase cases to send them to systran as parameters
        """
        output = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):  # ignore private
                output[snake_to_camel_case(key)] = value
        return output

    def _call_url(self, endpoint):
        """
        Returns the full call url: host + endpoint
        """
        return '{}{}'.format(SYSTRANIO_URL, endpoint)

    def _response(self, response):
        """
        Handles requests' response.
        Returns the json response or raises an exception
        """
        if response.status_code == 200:
            return response.json()
        if response.status_code == 500:
            try:
                result = response.json()
                raise ApiFailure(result['error']['message'])
            except ValueError:
                raise ApiFailure('Unknown error')
        if response.status_code == 400:
            raise ApiKeyError('Invalid API key : {}'.format(self.key))

    def post(self, endpoint):
        """
        Sends a POST request to systran with all the parameters
        previously set.
        """
        return self._response(
            requests.post(self._call_url(endpoint), data=self.payload))

    def get(self, endpoint):
        """
        Sends a GET request to systran with all the parameters
        previously set. Returns the json response or raises an exception
        """
        return self._response(
            requests.get(self._call_url(endpoint), data=self.payload))
