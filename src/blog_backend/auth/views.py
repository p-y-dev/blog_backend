from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.conf import settings
from blog_backend.errors import exceptions

from . import serializers
from .models import ConfirmationEmail
from blog_backend.utils import forming_url_with_params
from .tasks import user_send_activation_email


@swagger_auto_schema(
    method='post',
    operation_summary='Отправка ссылки для подтверждения почты.',
    operation_description='Отправляет ссылку на email, для его подтверждения.',
    request_body=serializers.ReqSendConfirmEmailSerializer,
    responses={
        status.HTTP_200_OK: ''
    }
)
@api_view(['POST'])
def send_confirm_email(request):
    serializer = serializers.ReqSendConfirmEmailSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    with transaction.atomic():
        try:
            client_url = settings.URL_CLIENT_CONFIRM_EMAIL
            if not client_url:
                raise exceptions.Conflict(exceptions.URL_CLIENT_CONFIRM_EMAIL_NOT_SET)
        except AttributeError:
            raise exceptions.Conflict(exceptions.URL_CLIENT_CONFIRM_EMAIL_NOT_SET)

        type_confirm = serializer.validated_data.pop('type')
        email = serializer.validated_data['email']

        ConfirmationEmail.objects.update_or_create(email=email, defaults=serializer.validated_data)

        get_params = {'confirm_code': serializer.validated_data['confirm_code'], 'type': type_confirm}
        url_email_confirm = forming_url_with_params(client_url, get_params)

        user_send_activation_email.delay(email, url_email_confirm)

    return Response(status=status.HTTP_200_OK)
