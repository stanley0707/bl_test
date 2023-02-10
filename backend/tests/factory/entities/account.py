from tests.factory.registry import register_factory_method


@register_factory_method(name="get_fake_account")
def get_fake_account(self, **kwargs):
    return {
        "username": self.fake.unique.email(),
        "password": self.fake.unique.password(),
        "role": "user",
        "first_name": self.fake.unique.first_name(),
        "last_name": self.fake.unique.last_name(),
    }
