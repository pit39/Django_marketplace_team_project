from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from shop.models import ShopProduct


class ProductInCart(models.Model):
    """Модель товара, хранящегося в корзине у пользователя"""
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='user_carts',
        verbose_name=_('владелец корзины')
    )

    shop_product = models.ForeignKey(
        to=ShopProduct,
        on_delete=models.CASCADE,
        related_name='user_cart_shops',
        verbose_name=_('модель, связывающая товар и магазин')
    )

    quantity = models.PositiveIntegerField(verbose_name=_('количество'), default=0)

    class Meta:
        verbose_name = _('корзина пользователя')
        verbose_name_plural = _('корзины пользователей')

    def __str__(self):
        return f'Товар {self.shop_product.product.name} в корзине у {self.user.email}'
