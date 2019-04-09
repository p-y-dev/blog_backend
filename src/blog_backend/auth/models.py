import uuid

from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ConfirmationEmail(models.Model):
    # 30 минут
    LIFE_TIME_SECONDS = 1800

    confirm_code = models.CharField(verbose_name=_('Код подтверждения'), default=uuid.uuid4, unique=True,
                                    max_length=1024)
    created_at = models.DateTimeField(verbose_name=_('Дата создания кода подтверждения'), default=timezone.now)
    email = models.EmailField(verbose_name=_('Email адрес'), unique=True)
    confirm = models.BooleanField(verbose_name=_('Подтвержден?'), default=False)

    class Meta:
        verbose_name = _('Подтверждение емейла')
        verbose_name_plural = _('Подтверждение емейлов')

    def __str__(self):
        return self.email
