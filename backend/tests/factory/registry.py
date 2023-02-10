_registry = dict()

__all__ = ["register_factory_method"]


class NotFound(Exception):
    pass


def register_factory_method(name: str):
    """
    Register factory method to be accessable in factory class
    """

    def decorator(method):
        _registry[name] = method
        return method

    return decorator


def get(name):
    method = _registry.get(name)
    if not method:
        raise NotFound(f"Factory method for {name} not found.")

    return method


def available():
    return list(_registry.keys())
