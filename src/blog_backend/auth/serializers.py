import os
import uuid
from enum import Enum

from django.utils import timezone
from rest_framework import serializers

from blog_backend.account.models import Account
from blog_backend.errors import validation


def generate_token(val) -> str:
    """
    Создание уникального токена

    :param val: Значение, которое будет участвовать в случайной генерации
    :return: Возвращает случайный токен
    """

    return str(uuid.UUID(bytes=os.urandom(16), version=4)) + str(val)


class ReqSendConfirmEmailSerializer(serializers.Serializer):
    class Type(Enum):
        reg = 'reg'
        reset_pass = 'reset_pass'

    TYPE_CHOICES = [(type.name, type.value) for type in list(Type)]

    email = serializers.EmailField(label='email пользователя', max_length=254)
    type = serializers.ChoiceField(label='Тип подтверждения email', choices=TYPE_CHOICES, default=Type.reg.reg.name)

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data['email']
        type_confirm = validated_data['type']

        account_exists = Account.objects.filter(email=email).exists()

        if type_confirm == self.Type.reg.name and account_exists:
            raise serializers.ValidationError({'email': validation.EMAIL_ALREADY_EXISTS})

        if type_confirm == self.Type.reset_pass.name and not account_exists:
            raise serializers.ValidationError({'email': validation.EMAIL_NOT_FOUND})

        validated_data['confirm_code'] = generate_token(email)
        validated_data['created_at'] = timezone.now()

        return validated_data
