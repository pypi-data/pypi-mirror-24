import abc
import six


@six.add_metaclass(abc.ABCMeta)
class MarvelResource:
    """
    Marvel Abstract Resource

    This abstract class is the abstraction for the marvel resources. Each of the resource have endpoints
    to comics, characters, events, series, stories and creators. There might be resources without one of the
    features, then the child class has to implement it accordingly.
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        """
        Get one
        :param resource_id: item id
        :return: return the given item
        """
        pass

    @abc.abstractmethod
    def comics(self):
        """
        Get all comics in the resource
        :param resource_id: item id
        :return: a lit of items
        """
        pass
        pass
