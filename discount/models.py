from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from .tools import load_images

DISCOUNT_TYPE_CHOICES = (
    ('percent', _('процент')),
    ('sum', _('сумма')),
    ('fixed', _('фиксированная цена')),
)

GROUP_CHOICES = (
    (1, _('первая группа')),
    (2, _('вторая группа')),
)

CART_CONDITION_CHOICES = (
    ('amount', _('количество товаров')),
    ('sum', _('сумма')),
)


class BaseDiscount(models.Model):
    """ Базовый класс скидки """

    title = models.CharField(max_length=100, verbose_name=_('заголовок'))
    description = models.CharField(max_length=1000, verbose_name=_('описание'))
    start = models.DateTimeField(verbose_name=_('время начала'), blank=True, null=True)
    end = models.DateTimeField(verbose_name=_('время окончания'), blank=True, null=True)
    type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name=_('тип скидки'))
    value = models.DecimalField(
        decimal_places=2, max_digits=8, validators=(MinValueValidator(1),), verbose_name=_('значение скидки'))
    priority = models.PositiveSmallIntegerField(validators=(MaxValueValidator(100),),
                                                default=0, verbose_name=_('приоритет скидки'))
    active = models.BooleanField(default=True, verbose_name=_('активность'))
    image = models.ImageField(upload_to=load_images, verbose_name=_('лого'))

    def clean_fields(self, exclude=None):
        if self.type == 'percent' and self.value > 99:
            raise ValidationError(_('скидка на процент не может быть больше 99'))
        super(BaseDiscount, self).clean_fields(exclude)

    class Meta:
        abstract = True


class BaseRelation(models.Model):
    discount = models.ForeignKey('ProductDiscount', on_delete=models.CASCADE, verbose_name=_('скидка'))

    class Meta:
        abstract = True


class BasePackRelation(models.Model):
    discount = models.ForeignKey('PackDiscount', on_delete=models.CASCADE, verbose_name=_('скидка'))
    group = models.PositiveSmallIntegerField(choices=GROUP_CHOICES, verbose_name=_('группа товаров'))

    class Meta:
        abstract = True


class ProductDiscount(BaseDiscount):
    products = models.ManyToManyField('product.Product', through='DiscountedProduct', verbose_name=_('товары'))
    categories = models.ManyToManyField('category.Category', through='DiscountedCategory', verbose_name=_('категории'))

    class Meta:
        verbose_name = _('скидка на товары')
        verbose_name_plural = _('скидки на товары')

    def __str__(self):
        return f'скидка на товары, тип {self.type}: {self.value}, приоритет - {self.priority}'

    def get_absolute_url(self):
        return reverse('product-discount', kwargs={'pk': self.pk})


class DiscountedProduct(BaseRelation):
    product = models.ForeignKey('product.Product', related_name='discounts',
                                on_delete=models.CASCADE, verbose_name=_('продукт'))

    def __str__(self):
        return f'скидка {self.discount.id}, товар {self.product.name}'


class DiscountedCategory(BaseRelation):
    category = models.ForeignKey('category.Category', related_name='discounts',
                                 on_delete=models.CASCADE, verbose_name=_('категория'))

    def __str__(self):
        return f'скидка {self.discount.id}, категория {self.category.name}'


class PackDiscount(BaseDiscount):
    products = models.ManyToManyField('product.Product', through='DiscountedPackProduct', verbose_name=_('товары'))
    categories = models.ManyToManyField('category.Category', through='DiscountedPackCategory',
                                        verbose_name=_('категории'))

    class Meta:
        verbose_name = _('скидка на наборы')
        verbose_name_plural = _('скидки на наборы')

    def __str__(self):
        return f'скидка на набор, тип {self.type}: {self.value}, приоритет - {self.priority}'

    def get_absolute_url(self):
        return reverse('pack-discount', kwargs={'pk': self.pk})


class DiscountedPackProduct(BasePackRelation):
    product = models.ForeignKey('product.Product', related_name='pack_discounts',
                                on_delete=models.CASCADE, verbose_name=_('продукт'))

    def __str__(self):
        return f'продукт {self.product_id}, скидка {self.discount_id} группа {self.group}'


class DiscountedPackCategory(BasePackRelation):
    category = models.ForeignKey('category.Category', related_name='pack_discounts',
                                 on_delete=models.CASCADE, verbose_name=_('категория'))

    def __str__(self):
        return f'категория {self.category_id}, скидка {self.discount_id} группа {self.group}'


class CartDiscount(BaseDiscount):
    condition = models.CharField(max_length=20, choices=CART_CONDITION_CHOICES, verbose_name=_('условие срабатывания'))
    condition_min_value = models.PositiveIntegerField(validators=(MinValueValidator(1),),
                                                      verbose_name=_('минимальное значение условия'))
    condition_max_value = models.PositiveIntegerField(validators=(MinValueValidator(1),),
                                                      verbose_name=_('максимальное значение условия'))

    class Meta:
        verbose_name = _('скидка на корзину')
        verbose_name_plural = _('скидки на корзину')

    def __str__(self):
        return f'скидка на корзину, тип {self.type}: {self.value}, приоритет - {self.priority}'

    def get_absolute_url(self):
        return reverse('cart-discount', kwargs={'pk': self.pk})

    def clean_fields(self, exclude=None):
        if self.condition_max_value < self.condition_min_value:
            raise ValidationError(_('максимальное значение условия должно быть больше или равно минамальному'))
        super(CartDiscount, self).clean_fields(exclude)
