import logging
import os
import time
from hashlib import md5

import requests
from requests import HTTPError

from marvelator.marvel_resource import MarvelResource


class MarvelCloudResource(MarvelResource):
    """
    Marvel Cloud Resource

    This class abstracts the cloud API calls for gathering resources. Every marvel resource has the structure:

    - GET /v1/public/characters
    - GET /v1/public/characters/{characterId}
    - GET /v1/public/characters/{characterId}/comics
    - GET /v1/public/characters/{characterId}/events
    - GET /v1/public/characters/{characterId}/series
    - GET /v1/public/characters/{characterId}/stories
    - ...

    The idea is to have the generic implementation here and a more specific ones inside each specialist class.

    """
    def __init__(self):
        MarvelResource.__init__(self)

        self.api = 'https://gateway.marvel.com/v1/public/'
        self.resource_name = None
        self.resource_id = None

        self.public_key = os.environ.get('MARVEL_PUB_KEY', '')
        self.private_key = os.environ.get('MARVEL_PRIV_KEY', '')

    def get_from_marvel(self, endpoint, additional_params=None):
        """
        Get data from the Marvel servers

        :param endpoint: the endpoint specifier
        :param additional_params: additional params for the GET request
        :return: the request result
        """
        ts = str(int(time.time()))
        url = self.api + endpoint

        params = {
            'ts': ts,
            'apikey': self.public_key,
            'hash': md5(ts + self.private_key + self.public_key).hexdigest(),
        }

        # if additional params were passed, update the default params
        if additional_params is not None:
            params.update(additional_params)

        return requests.get(url, params)

    def get(self):
        """
        Get a single resource
        :return: a dict with the resource
        """
        endpoint_specifier = str(self.resource_name) + '/' + str(self.resource_id)

        try:
            response = self.get_from_marvel(endpoint_specifier)
            response.raise_for_status()
        except HTTPError as e:
            logging.warning(str(e.message))
            raise e

        item = response.json().get('data').get('results')[0]
        header = {'attributionHTML': response.json().get('attributionHTML'),
                  'attributionText': response.json().get('attributionText')}

        item_plus_header = {}
        item_plus_header.update(item)
        item_plus_header.update(header)

        return item_plus_header

    def comics(self, max_items=1000):
        """
        Get the comics from a resource.
        This method returns a dict vector instead of Comic instances. This is a trade off as
        for now the instances or not needed.

        :return: a list of dict with the comics
        """
        endpoint_specifier = str(self.resource_name) + '/' + str(self.resource_id) + '/comics'
        comics_list = []

        limit = 100
        count = 100
        offset = 0

        while count == limit and offset < max_items:
            try:
                response = self.get_from_marvel(endpoint_specifier, {'limit': limit, 'offset': offset})
                response.raise_for_status()
            except HTTPError as e:
                logging.warning(str(e.message))
                raise e

            response_json = response.json()

            comics_list.extend(response_json.get('data').get('results'))

            count = response_json.get('data').get('count')
            offset += count

        return comics_list
