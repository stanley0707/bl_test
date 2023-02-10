from tests.factory.registry import register_factory_method


@register_factory_method(name="get_fake_event")
def get_fake_event(self, **kwargs):
    return {}
