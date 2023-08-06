from marvelator.marvel_cloud_resource import MarvelCloudResource


class Character:
    """
    A Character
    Represents a marvel character.
    """
    def __init__(self):
        # The story's description
        self.name = None

        # A list of names and pictures of the characters that features in the story
        self.thumbnail = []

        # header informations
        self.attributionHTML = None
        self.attributionText = None

    def load_from_dict(self, char_data):
        """
        Load data from dict.
        :param char_data: a dict with the dict
        :return: character
        """
        self.name = char_data.get('name')
        self.thumbnail = char_data.get('thumbnail')

        # header info
        self.attributionHTML = char_data.get('attributionHTML')
        self.attributionText = char_data.get('attributionText')

        return self


class CharactersResource(MarvelCloudResource):
    """
    Character Resource

    This class implements the MarvelCloudResource. It is an abstraction for the Marvel API dealing
    with character specific implementations.
    """
    def __init__(self, character_id=None):
        MarvelCloudResource.__init__(self)

        self.resource_id = character_id
        self.resource_name = 'characters'

    def get(self):
        """
        Get a character
        Call the superclass for getting the character cloud response and build a character
        :return: character
        """
        char = Character().load_from_dict(MarvelCloudResource.get(self))
        return char
