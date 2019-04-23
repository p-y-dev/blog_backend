from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers

from blog_backend.auth.models import ConfirmationEmail
from blog_backend.errors import validation
from blog_backend.utils import life_time_is_correct, jwt_encode
from .models import Account

regex_password = r'(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{6,}'


def validate_password(validate_data):
    password = validate_data.get('password')
    confirm_password = validate_data.get('confirm_password')

    if confirm_password != password:
        raise serializers.ValidationError({
            'password': [validation.PASSWORDS_DO_NOT_MATCH],
            'confirm_password': [validation.PASSWORDS_DO_NOT_MATCH]
        })

    validate_data.pop('confirm_password')
    validate_data['password'] = make_password(password)

    return validate_data


class ReqRegistrationAccountSerializer(serializers.ModelSerializer):
    password = serializers.RegexField(regex=regex_password)
    confirm_password = serializers.RegexField(regex=regex_password)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = Account
        exclude = 'id', 'datetime_reg'

    @staticmethod
    def validate_email(email):
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError(validation.EMAIL_ALREADY_EXISTS)

        confirm_email_data = ConfirmationEmail.objects.filter(email=email, confirm=True)
        if not confirm_email_data.exists():
            raise serializers.ValidationError(validation.EMAIL_CONFIRM_DATA_NOT_FOUND)

        confirm_email_data = confirm_email_data.get()

        if not life_time_is_correct(confirm_email_data.LIFE_TIME_SECONDS, confirm_email_data.created_at):
            raise serializers.ValidationError({'confirm_code': validation.CODE_EXPIRED})

        return email

    def validate(self, data):
        validate_data = super().validate(data)
        return validate_password(validate_data)


class AccountSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(label='Токен доступа')

    class Meta:
        model = Account
        fields = 'id', 'email', 'sex', 'first_name', 'last_name', 'middle_name', 'date_birth', 'access_token'

    @staticmethod
    def get_access_token(obj):
        return jwt_encode(obj.email)


class ReqLoginSerializer(serializers.Serializer):
    login = serializers.EmailField(max_length=254)
    password = serializers.CharField(min_length=1)

    def validate(self, data):
        validate_data = super().validate(data)
        login = validate_data.pop('login')
        password = validate_data.pop('password')

        account = Account.objects.filter(email=login)
        if not account.exists():
            raise serializers.ValidationError({
                'login': [validation.USER_NOT_FOUND],
            })

        account = account.get()

        if not check_password(password, account.password):
            raise serializers.ValidationError({
                'password': [validation.USER_INVALID_PASSWORD],
            })

        return account


class ReqResetPasswordSerializer(serializers.Serializer):
    confirm_code = serializers.CharField(label='Код подтверждения, отправленный на почту', max_length=1024)
    password = serializers.RegexField(label='Пароль', regex=regex_password)
    confirm_password = serializers.RegexField(label='Подтверждения пароля', regex=regex_password)

    def validate(self, data):
        validate_data = validate_password(super().validate(data))

        confirm_email_query = ConfirmationEmail.objects.filter(
            confirm_code=validate_data.pop('confirm_code'),
            confirm=True
        )
        if not confirm_email_query.exists():
            raise serializers.ValidationError({'confirm_code': [validation.EMAIL_CONFIRM_DATA_NOT_FOUND]})

        confirm_email_data = confirm_email_query.values('email').get()
        account_query = Account.objects.filter(email=confirm_email_data['email'])
        if not account_query.exists():
            raise serializers.ValidationError({'detail': [validation.USER_NOT_FOUND]})

        validate_data['account_query'] = account_query
        validate_data['confirm_email_query'] = confirm_email_query
        return validate_data
