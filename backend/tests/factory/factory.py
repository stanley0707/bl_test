from functools import partial

import tests.factory.entities  # noqa

from faker import Faker
from . import registry


class Factory:
    fake = Faker()

    def cycle(self, count):
        """
        Run given method X times:
            Factory.cycle(5).orderItem()  # gives 5 orders
        """
        return CycleFactory(self, count)

    def __getattr__(self, name):
        return partial(registry.get(name), self)

    def __getitem__(self, name):
        return partial(registry.get(name), self)


class CycleFactory:
    """
    Simple factory wrapper to call method for N times
    """

    def __init__(self, factory: Factory, count: int):
        self.factory = factory
        self.count = count

    def __getattr__(self, name):
        if hasattr(self.factory, name):
            return lambda *args, **kwargs: [
                getattr(self.factory, name)(*args, **kwargs)
                for _ in range(0, self.count)
            ]
