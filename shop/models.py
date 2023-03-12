from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Product
from users.models import CustomUser


class Shop(models.Model):
    """Магазин"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    holder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="shops", verbose_name=_("владелец"))
    address = models.TextField(blank=True, null=True, verbose_name=_("адрес"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("почта"))
    validator_phone = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=' '.join([str(_('Телефон должен быть введён в формате:')), '+777777777777',
                          str(_('Максимально количество цифр - 15'))]))
    phone = models.CharField(max_length=16, blank=True, validators=[validator_phone], null=True, verbose_name=_("телефон"))
    description = models.TextField(blank=True, null=True, verbose_name=_("описание"))
    logo = models.ImageField(upload_to="logo", null=True, verbose_name=_("логотип"))
    slug = models.SlugField(unique=True, verbose_name=_("слаг"))

    def __str__(self):
        return f"Магазин {self.name}"

    class Meta:
        verbose_name = _("магазин")
        verbose_name_plural = _("магазины")


class ShopProduct(models.Model):
    """Модель продукта магазина"""

    store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_products", verbose_name=_("магазин"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="shop_products", verbose_name=_("продукт")
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("цена"))
    old_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("старая цена"))
    amount = models.IntegerField(default=0, verbose_name=_("количество"))
    add_at = models.DateTimeField(auto_now_add=True, verbose_name=_("дата добавления"))

    def __str__(self):
        return f"Продукт {self.product} из магазина {self.store}"

    class Meta:

        verbose_name = _('Продукт магазина')
        verbose_name_plural = _('Продукты магазина')

