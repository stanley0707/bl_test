import logging
import abc

from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError()


class BaseManager(BaseCRUD, abc.ABC):
    """
    Functional manager. Work with model classes and
    block CRUD or another special realization in instance.
    """

    def __init__(self, object_type=None):
        self.model = object_type
        self.session: AsyncSession = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def __get__(self, obj, object_type):
        if obj is None:
            self.model = object_type
        else:
            raise AttributeError(
                "Manger isn't accessible via {} instances".format(object_type)
            )
        return self
