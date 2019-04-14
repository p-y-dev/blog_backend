from enum import Enum

from django.utils import timezone
from rest_framework import serializers

from blog_backend.account.models import Account
from blog_backend.errors import validation
from blog_backend.utils import life_time_is_correct, generate_token
from .models import ConfirmationEmail


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


class ReqConfirmEmailSerializer(serializers.Serializer):
    confirm_code = serializers.CharField(min_length=1, max_length=1024)

    def validate(self, data):
        validated_data = super().validate(data)
        confirm_code = validated_data.pop('confirm_code')

        confirmation_email_obj = ConfirmationEmail.objects.filter(confirm_code=confirm_code)

        if not confirmation_email_obj.exists():
            raise serializers.ValidationError({'confirm_code': validation.CODE_NOT_FOUND})
        confirmation_email_obj = confirmation_email_obj.get()

        if not life_time_is_correct(confirmation_email_obj.LIFE_TIME_SECONDS, confirmation_email_obj.created_at):
            raise serializers.ValidationError({'confirm_code': validation.CODE_EXPIRED})

        if confirmation_email_obj.confirm:
            raise serializers.ValidationError({'confirm_code': validation.EMAIL_CODE_ALREADY_CONFIRMED})

        validated_data['confirmation_email'] = confirmation_email_obj

        return validated_data


class ConfirmEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationEmail
        fields = 'confirm', 'email'
