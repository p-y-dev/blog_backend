import factory
from django.contrib.auth.hashers import make_password
from faker import Factory

from .models import Account

faker = Factory.create()


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    email = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()
    middle_name = faker.name()
    password = make_password(faker.password())
