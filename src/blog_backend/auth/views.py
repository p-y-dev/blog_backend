from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import serializers


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

    return Response(status=status.HTTP_200_OK)
