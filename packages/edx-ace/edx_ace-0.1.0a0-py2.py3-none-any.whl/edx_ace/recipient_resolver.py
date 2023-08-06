# lint-amnesty, pylint: disable=missing-docstring
import six

from abc import ABCMeta, abstractmethod  # lint-amnesty, pylint: disable=wrong-import-order


# TODO(now): Do we even need to define this class? It seems like something the client could manage on their own.
@six.add_metaclass(ABCMeta)
class RecipientResolver(object):

    @abstractmethod
    def send(self, msg_type, *args, **kwargs):
        pass
