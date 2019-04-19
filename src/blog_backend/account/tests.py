from django.urls import reverse
from faker import Factory
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.test import APITestCase

from blog_backend.auth.factories import ConfirmationEmailFactory
from blog_backend.errors import validation
from .factories import AccountFactory
from .models import Account
from blog_backend.utils import jwt_encode, jwt_decode


faker = Factory.create()


class TestsRegistration(APITestCase):
    def setUp(self):
        password = 'Qwtgf123Hhgjd'
        self.url_registration = reverse('account:registration')

        self.request_data_registration = {
            'email': '',
            'phone': '',
            'sex': Account.Sex.male.name,
            'date_birth': '1990-01-01',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': password,
            'confirm_password': password,
        }

    def test_registration(self):
        """
        Регистрация пользователя в системе
        """

        email = ConfirmationEmailFactory().email
        request_data = self.request_data_registration.copy()
        request_data['email'] = email

        response = self.client.post(self.url_registration, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Ошибка при регистрации аккаунта!')

        if not Account.objects.filter(email=email).exists():
            self.fail('Аккаунт не создался в системе!')

        jwt_token = jwt_encode(email)

        if response.json()['access_token'] != jwt_token:
            self.fail('Сгенерирован неверный jwt токен')

        if response.json()['email'] != jwt_decode(jwt_token):
            self.fail('Расшифрован неверный email по jwt токену')

    def test_registration_email_already_exists(self):
        """
        Проверка валидатора при регистрации, на то,
        что он отработает, если в системе есть аккаунт с регистрируемым email
        """

        account = AccountFactory()
        request_data = self.request_data_registration.copy()
        request_data['email'] = account.email

        response = self.client.post(self.url_registration, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()

        if response_data['email'][0] != validation.EMAIL_ALREADY_EXISTS:
            self.fail('Должен сработать валидатор, в системе есть пользователь с таким e-mail!')

    def test_registration_confirm_data_not_found(self):
        """
        Проверка валидатора при регистрации, на то,
        что он отработает, если в системе e-mail не подтверждены, или вовсе отсутствует объект подтверждения
        """

        request_data = self.request_data_registration.copy()

        # Нет объекта подтверждения в системе
        request_data['email'] = faker.email()

        response = self.client.post(self.url_registration, request_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        if response_data['email'][0] != validation.EMAIL_CONFIRM_DATA_NOT_FOUND:
            self.fail('Должен сработать валидатор, не подтвержден e-mail!')

        # Объекты подтверждения присутствуют в системе, но не подтверждены
        email = ConfirmationEmailFactory(confirm=False).email
        request_data['email'] = email

        response = self.client.post(self.url_registration, request_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        if response_data['email'][0] != validation.EMAIL_CONFIRM_DATA_NOT_FOUND:
            self.fail('Должен сработать валидатор, не подтвержден e-mail!')

    def test_registration_passwords_do_not_match(self):
        """
        Проверка валидатора при регистрации, на то,
        что он отработает, если пароли не совпадают
        """

        email = ConfirmationEmailFactory().email

        request_data = self.request_data_registration.copy()
        request_data['email'] = email
        request_data['confirm_password'] = 'KJhkhdhg32hjhGh'

        response = self.client.post(self.url_registration, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()

        if response_data['password'][0] != validation.PASSWORDS_DO_NOT_MATCH:
            self.fail('Должен сработать валидатор, пароли не совпадают!')

        if response_data['confirm_password'][0] != validation.PASSWORDS_DO_NOT_MATCH:
            self.fail('Должен сработать валидатор, пароли не совпадают!')


class TestsLogin(APITestCase):
    def setUp(self):
        self.user_password = 'LKjddkjk234lkdawlkj'
        self.account = AccountFactory(password=make_password(self.user_password))

        self.url = reverse('account:login')
        self.request_data = {
            'login': self.account.email,
            'password': self.user_password
        }

    def test_login(self):
        """
        Авторизации пользователя в системе
        """

        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Ошибка при авторизации пользователя!')

        jwt_token = jwt_encode(self.account.email)

        if response.json()['access_token'] != jwt_token:
            self.fail('Сгенерирован неверный jwt токен')

    def test_login_user_not_found(self):
        """
        Проверка валидатора при входе в систему, на то,
        что он отработает, если в системе нет аккаунта с данным логином, или введен неверный пароль
        """

        request_data = self.request_data.copy()

        # Авторизация с неверным логином
        request_data['login'] = 'awaljdlawj@madawd.ru'

        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()

        if response_data['login'][0] != validation.USER_NOT_FOUND:
            self.fail('Должен сработать валидатор, в системе отсутвует пользователь с данным логином!')

        # Авторизация с неверным паролем
        request_data['login'] = self.account.email
        request_data['password'] = 'ladjlwj876IKUYi22'
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()

        if response_data['password'][0] != validation.USER_INVALID_PASSWORD:
            self.fail('Должен сработать валидатор, в системе отсутвует пользователь с данным паролем!')


class TestAccount(APITestCase):
    def test_reset_password(self):
        old_password = 'DGmahsgfd12gfhg'
        account = AccountFactory(password=make_password(old_password))
        confirm_email = ConfirmationEmailFactory(email=account.email)

        new_password = 'QweasdAsd434gGYtfdaw'
        request_data = {
            'confirm_code': confirm_email.confirm_code,
            'password': new_password,
            'confirm_password': new_password
        }
        url = reverse('account:reset_password')

        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Ошибка при обновление пароля')

        account = Account.objects.get(id=account.id)

        if check_password(old_password, account.password) or not check_password(new_password, account.password):
            self.fail('Пароль не обновился!')
