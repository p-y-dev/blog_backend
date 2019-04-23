from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from blog_backend.auth.models import ConfirmationEmail

from blog_backend.auth.jwt_auth import AuthJWT
from . import serializers
from .models import Account


@swagger_auto_schema(
    method='get',
    operation_summary='Получение данных пользователя',
    operation_description='Получение данных пользователя',
    responses={
        status.HTTP_200_OK: serializers.AccountSerializer
    }
)
@api_view(['GET'])
@authentication_classes((AuthJWT,))
def account(request):
    return Response(serializers.AccountSerializer(request.user).data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_summary='Регистрация пользователя в системе.',
    operation_description='Регистрация пользователя в системе.',
    request_body=serializers.ReqRegistrationAccountSerializer,
    responses={
        status.HTTP_201_CREATED: serializers.AccountSerializer
    }
)
@api_view(['POST'])
def registration(request):
    serializer = serializers.ReqRegistrationAccountSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    with transaction.atomic():
        account_obj = Account.objects.create(**serializer.validated_data)
        ConfirmationEmail.objects.filter(email=account_obj.email).delete()
        account_obj = serializers.AccountSerializer(account_obj).data

    return Response(account_obj, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    operation_summary='Вход пользователя в систему',
    operation_description='Вход пользователя в систему.',
    request_body=serializers.ReqLoginSerializer,
    responses={
        status.HTTP_200_OK: serializers.AccountSerializer
    }
)
@api_view(['POST'])
def login(request):
    serializer = serializers.ReqLoginSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    account_obj = serializer.validated_data
    return Response(serializers.AccountSerializer(account_obj).data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_summary='Сброс пароля у неавторизованного пользователя',
    operation_description='Сброс пароля у неавторизованного пользователя',
    request_body=serializers.ReqResetPasswordSerializer,
    responses={
        status.HTTP_200_OK: ''
    }
)
@api_view(['POST'])
def reset_password(request):
    serializer = serializers.ReqResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    with transaction.atomic():
        serializer.validated_data['account_query'].update(password=serializer.validated_data['password'])
        serializer.validated_data['confirm_email_query'].delete()

    return Response(status=status.HTTP_200_OK)
