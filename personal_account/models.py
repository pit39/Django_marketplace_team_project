from django.db import models

from product.models import Product
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class ViewsHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('продукт'))

    class Meta:
        verbose_name = _('история просмотров')

    def __str__(self):
        return self.product.name
