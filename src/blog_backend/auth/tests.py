from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ConfirmationEmail

faker = Factory.create()


class TestsAuth(APITestCase):
    def test_send_confirm_email(self):
        """
        Отправка ссылки для подтверждения e-mail
        """

        email = faker.email()
        request_data = {'email': email}
        url = reverse('auth:send_confirm_email')

        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Ошибка при отправке ссылки подтверждения на почту')

        if not ConfirmationEmail.objects.filter(email=email).exists():
            self.fail('После отправки ссылке для подтверждения e-mail, в базе не создался объект подтверждения!')
