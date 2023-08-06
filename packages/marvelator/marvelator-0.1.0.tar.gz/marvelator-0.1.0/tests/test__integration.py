from unittest import TestCase

import os

from marvelator.characters_resource import CharactersResource
from marvelator.comics_resource import ComicsResource


class TestIntegrations(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIntegrations, self).__init__(*args, **kwargs)

        self.private_key = os.environ.get('MARVEL_PRIV_KEY')
        self.public_key = os.environ.get('MARVEL_PUB_KEY')

    def test_get_comic(self):
        comic = ComicsResource(64293).get()

        self.assertIsNotNone(comic)

    def test_get_character(self):
        char = CharactersResource(1009515).get()

        self.assertIsNotNone(char)

    def test_get_comics_of_char(self):
        comics = CharactersResource(1009282).comics()
        self.assertGreater(len(comics), 1)
