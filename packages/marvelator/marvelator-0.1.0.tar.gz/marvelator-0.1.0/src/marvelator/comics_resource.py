from marvelator.marvel_cloud_resource import MarvelCloudResource


class Comic:
    """
    A Comic
    Represents a marvel comic.
    """
    def __init__(self):
        # The story's description
        self.description = None

        # A list of names and pictures of the characters that features in the story
        self.features = []

    def load_from_dict(self, comic_data):
        """
        Load data from dict.
        :param comic_data: a dict with the dict
        :return: comic
        """
        self.description = comic_data.get('description')
        self.features = comic_data.get('characters')

        return self


class ComicsResource(MarvelCloudResource):
    """
    Character Resource

    This class implements the MarvelCloudResource. It is an abstraction for the Marvel API dealing
    with comic specific implementations.
    """
    def __init__(self, comic_id=None):
        MarvelCloudResource.__init__(self)

        self.resource_id = comic_id
        self.resource_name = 'comics'

    def get(self):
        """
        Get a comic
        Call the superclass for getting the comic cloud response and build a comic
        :return: comic
        """
        comic = Comic().load_from_dict(MarvelCloudResource.get(self))
        return comic
