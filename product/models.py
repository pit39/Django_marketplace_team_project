from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from category.models import Category
from category.tools import get_slug

from . import tools
from . import utility


class Product(utility.ProductRatingMixin, utility.ProductPriceMixin, utility.ProductDiscountMixin, models.Model):

    """Модель товара"""
    name = models.CharField(max_length=512, unique=True, verbose_name=_('название'))
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    views = models.PositiveIntegerField(default=0, verbose_name=_('просмотры'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата обновления'))
    description = models.TextField(verbose_name=_('описание'))
    property = models.ManyToManyField('Property', through='ProductProperty', verbose_name=_('характеристики'))
    sort_index = models.PositiveSmallIntegerField(validators=(MaxValueValidator(1000),),
                                                  default=0, verbose_name=_('индекс сортировки'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> 'Product':
        self.slug: str = get_slug(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('продукт')
        verbose_name_plural = _('продукция')


class ProductProperty(models.Model):
    """Свойства продукта"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    property = models.ForeignKey('Property', on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_('значение'))

    def __str__(self):
        return 'product_property_{}'.format(self.pk)

    class Meta:
        verbose_name = _('характеристика продукта')
        verbose_name_plural = _('характеристики продукта')


class Property(models.Model):
    """Свойства"""
    name = models.CharField(max_length=512, verbose_name='характеристики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('характеристика')
        verbose_name_plural = _('характеристики')


class Image(models.Model):
    file = models.ImageField(upload_to=tools.load_images, verbose_name=_('файл'))
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='images', verbose_name=_('продукт'))

    def __str__(self):
        return f'{self.file.url}'

    class Meta:
        verbose_name = _('изображение продукта')
        verbose_name_plural = _('изображения продукта')


class Review(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='reviews', verbose_name=_('товар'))
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE,
                             related_name='reviews', verbose_name=_('пользователь'))
    text = models.CharField(max_length=1000, verbose_name=_('текст отзыва'))
    rating = models.SmallIntegerField(validators=(MinValueValidator(1), MaxValueValidator(5)),
                                      verbose_name=_('Оценка'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

    def __str__(self):
        return f'{self.user.full_name}: {self.rating}'
