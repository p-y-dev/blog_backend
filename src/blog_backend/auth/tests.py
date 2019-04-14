from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APITestCase

from blog_backend.account.factories import AccountFactory
from .factories import ConfirmationEmailFactory
from .models import ConfirmationEmail

faker = Factory.create()


class TestsAuth(APITestCase):
    def setUp(self):
        self.url_send_confirm_email = reverse('auth:send_confirm_email')

    def test_send_confirm_email(self):
        """
        Отправка ссылки для подтверждения e-mail
        """

        email = faker.email()
        request_data = {'email': email}

        response = self.client.post(self.url_send_confirm_email, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Ошибка при отправке ссылки подтверждения на почту')

        if not ConfirmationEmail.objects.filter(email=email).exists():
            self.fail('После отправки ссылке для подтверждения e-mail, в базе не создался объект подтверждения!')

    def test_send_confirm_email_validate(self):
        """
        Проверка на то, что сработает валидатор, если попытаться отправить ссылку
        подтверждения почты для регистрации, если в системе есть уже аккаунт с данным e-mail
        """

        account = AccountFactory()
        request_data = {
            'email': account.email
        }
        response = self.client.post(self.url_send_confirm_email, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         'Должен был сработать валидатор. В системе есть уже аккаунт с данным e-mail')

    def test_confirm_email(self):
        """
        Подтверждение e-mail
        """

        confirmation_email = ConfirmationEmailFactory(confirm=False)
        url = reverse('auth:confirm_email')
        request_data = {
            'confirm_code': confirmation_email.confirm_code
        }

        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Ошибка при подтверждения e-mail')

        if not ConfirmationEmail.objects.filter(confirm=True, email=confirmation_email.email).exists():
            self.fail('E-mail не был подтвержден!')
