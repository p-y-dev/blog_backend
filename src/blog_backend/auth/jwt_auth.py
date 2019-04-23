import jwt.exceptions as jwt_except
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from blog_backend.errors import exceptions
from blog_backend.utils import jwt_decode
from blog_backend.account.models import Account


class AuthJWT(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTH', None)
        if not access_token:
            raise AuthenticationFailed(exceptions.ACCESS_TOKEN_IS_ABSENT)

        try:
            email = jwt_decode(access_token)
            account = Account.objects.get(email=email)
        except (jwt_except.DecodeError, KeyError, Account.DoesNotExist):
            raise AuthenticationFailed(exceptions.ACCESS_TOKEN_NOT_FOUND)

        return account, None
