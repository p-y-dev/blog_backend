from enum import Enum

from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    class Sex(Enum):
        male = _('Мужской')
        female = _('Женский')

    SEX_CHOICES = [(sex.name, sex.value) for sex in list(Sex)]

    email = models.EmailField(verbose_name=_('Емейл'), unique=True)
    sex = models.CharField(verbose_name=_('Пол'), choices=SEX_CHOICES, max_length=12, null=True, default=None)
    first_name = models.CharField(verbose_name=_('Имя'), max_length=128)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=128)
    middle_name = models.CharField(verbose_name=_('Отчество'), max_length=128, blank=True, default='')
    password = models.CharField(_('Проль'), max_length=128)
    date_birth = models.DateField(verbose_name=_('Дата рождения'), null=True, default=None)

    datetime_reg = models.DateTimeField(verbose_name=_('Дата и время регстрации'), default=timezone.now)

    class Meta:
        verbose_name = _('Аккаунт')
        verbose_name_plural = _('Аккаунты')
        ordering = '-id',

    def __str__(self):
        return f'{self.email}'
