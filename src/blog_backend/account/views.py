from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from blog_backend.auth.models import ConfirmationEmail


from . import serializers
from .models import Account


@swagger_auto_schema(
    method='post',
    operation_summary='Регистрация в системе.',
    operation_description='Регистрация в системе.',
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
