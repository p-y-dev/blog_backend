from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT


URL_CLIENT_CONFIRM_EMAIL_NOT_SET = _('Не задан урл для подтверждения email пользователя. '
                                     'Обратитесь к разработчикам API.')
ACCESS_TOKEN_IS_ABSENT = _('Токен доступа отсутствует в запросе')
ACCESS_TOKEN_NOT_FOUND = _('Токен доступа не найден')
