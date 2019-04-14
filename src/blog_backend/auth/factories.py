import factory
from django.utils import timezone
from faker import Factory

from blog_backend.utils import generate_token
from .models import ConfirmationEmail

faker = Factory.create()


class ConfirmationEmailFactory(factory.DjangoModelFactory):
    class Meta:
        model = ConfirmationEmail

    email = faker.email()
    confirm_code = generate_token(email)
    created_at = timezone.now()
    confirm = True
