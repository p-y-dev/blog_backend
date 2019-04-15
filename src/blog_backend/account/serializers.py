from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from blog_backend.auth.models import ConfirmationEmail
from blog_backend.errors import validation
from blog_backend.utils import life_time_is_correct
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
    class Meta:
        model = Account
        exclude = 'password',
