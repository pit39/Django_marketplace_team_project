from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from category.models import Category
from product.models import Product
from .utility import FavouriteLowestPriceMixin


class Favourite(FavouriteLowestPriceMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='favourites', verbose_name=_('категория'))

    class Meta:
        verbose_name = _('избранная категория')
        verbose_name_plural = _('избранные категории')

    def __str__(self):
        return str(self.category)


class DayOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='day_offers', verbose_name=_('продукт'))
    day = models.DateField(default=timezone.now, verbose_name=_('день'))

    class Meta:
        verbose_name = _('предложение дня')
        verbose_name_plural = _('предложения дня')

    def __str__(self):
        return str(self.product)


class Top(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='top_products', verbose_name=_('продукт'))

    class Meta:
        verbose_name = _('популярный товар')
        verbose_name_plural = _('популярные товары')

    def __str__(self):
        return str(self.product)


class Hot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='hots', verbose_name=_('продукт'))

    class Meta:
        verbose_name = _('горячие предложение')
        verbose_name_plural = _('горячие предложения')

    def __str__(self):
        return str(self.product)


class Limit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='limits', verbose_name=_('продукт'))

    class Meta:
        verbose_name = _('ограниченное предложение')
        verbose_name_plural = _('ограниченные предложения')

    def __str__(self):
        return str(self.product)
