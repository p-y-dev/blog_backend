from django.utils.translation import gettext_lazy as _

EMAIL_ALREADY_EXISTS = _('Пользователь с таким емейлом уже существует')
EMAIL_NOT_FOUND = _('Пользователя с таким емейлом не существует')
EMAIL_CODE_ALREADY_CONFIRMED = _('Невозможно подтвердить E-mail, так как он уже был подтвержден')
EMAIL_CONFIRM_DATA_NOT_FOUND = _('Данные о подтверждении E-mail отсутствуют')

CODE_NOT_FOUND = _('Код не найден в системе')
CODE_EXPIRED = _('Код устарел')

PASSWORDS_DO_NOT_MATCH = _('Пароли не совпадают')

USER_NOT_FOUND = _('Пользователь не найден')
USER_INVALID_PASSWORD = _('Неверный пароль пользователя')
