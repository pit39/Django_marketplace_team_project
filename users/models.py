import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


def update_avatar(instance, filename):
    path = "avatars/"
    file_name = f'{instance.user.email}_avatar.{filename.split(".")[-1]}'
    return os.path.join(path, file_name)


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""
    username = None
    email = models.EmailField(verbose_name=_('электронная почта'), max_length=128, unique=True)
    validator_phone = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=' '.join([str(_('Телефон должен быть введён в формате:')), '+777777777777',
                          str(_('Максимально количество цифр - 15'))]))
    phone_number = models.CharField(verbose_name=_('телефон'), validators=[validator_phone], max_length=16, blank=True)
    full_name = models.CharField(verbose_name=_('ФИО'), max_length=256, blank=True)
    # avatar = models.ImageField(verbose_name=_('аватар'), upload_to=update_avatar)
    avatar = models.ImageField(verbose_name=_('аватар'), upload_to="users")
    is_staff = models.BooleanField(verbose_name=_('работник'), default=False)
    is_active = models.BooleanField(verbose_name=_('флаг активности'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

        permissions = (
            ('can_do_order', _('Может делать заказ')),
        )

    def __str__(self):
        return self.email
