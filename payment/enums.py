import random

from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.TextChoices):
    """Статусы заказа"""
    WAIT = 'w', _('Ожидание оплаты')
    FAIL = 'f', _('Не оплачен')


class ExecPayment:
    """Ошибки оплаты заказа"""
    EXEC = (
        _('Вашу карту зажевал банкомат'),
        _('Недостаточно средств'),
        _('Неверный CVC'),
        _('Это была необдуманная покупка, подумайте еще раз нужно ли оно вам'),
        _('Код ошибки 007, обратитесь в службу поддержки вашего банка'),
    )


def get_random_exc() -> str:
    """Функция возвращает случайную ошибку при неудачной оплате"""
    return random.choice(ExecPayment.EXEC)

