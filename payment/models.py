from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from order.models import Order
from payment.enums import PaymentStatus


class PaymentInfo(models.Model):
    """Модель неоплаченных заказов"""
    order = models.OneToOneField(
        to=Order,
        on_delete=models.CASCADE,
        related_name='payment_info',
        verbose_name=_('заказ')
    )

    status = models.CharField(
        max_length=1,
        choices=PaymentStatus.choices,
        default=PaymentStatus.WAIT,
        verbose_name=_('статус заказа')
    )

    cart_number = models.PositiveIntegerField(
        verbose_name=_('номер карты'),
        validators=[
            MinValueValidator(limit_value=10000000),
            MaxValueValidator(limit_value=99999999)
        ]
    )

    def __str__(self) -> str:
        return f'Статус заказа {self.order.id} - {self.status}'


class ErrorMessage(models.Model):
    """Модель с ошибкой оплаты заказа"""
    payment_info = models.OneToOneField(
        to=PaymentInfo,
        on_delete=models.CASCADE,
        related_name='error_message',
        verbose_name=_('неоплаченный заказ')
    )

    message = models.CharField(max_length=128, verbose_name=_('текст ошибки'))

    def __str__(self) -> str:
        return f'Текст ошибки оплаты к заказу {self.payment_info.order.id}'
