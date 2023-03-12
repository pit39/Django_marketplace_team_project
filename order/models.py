import decimal

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from product.models import Product
from users.models import CustomUser

DELIVERY_CHOICES = [("обычная", _("Обычная доставка")), ("экспресс", _("Экспресс доставка"))]
# validator_number = RegexValidator(regex=r'^\+?1?\d{9,15}$',
#                                     message='Номер должен быть в следующем формате: +77777777777')


class PaymentChoices(models.TextChoices):
    card = "card", _("Онлайн картой")
    random = "random", _("Онлайн со случайного чужого счёта")


class Order(models.Model):
    consumer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders", verbose_name=_("потребитель")
    )
    first_second_names = models.TextField(null=True, blank=True, verbose_name=_("ФИО"))
    validator_phone = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=' '.join([str(_('Телефон должен быть введён в формате:')), '+777777777777',
                                                   str(_('Максимально количество цифр - 15'))]))
    phone = models.CharField(null=True, blank=True, validators=[validator_phone], max_length=16, verbose_name=_("телефон"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("почта"))
    delivery = models.CharField(max_length=10, default="обычная", choices=DELIVERY_CHOICES, verbose_name=_("доставка"))
    payment = models.CharField(max_length=10, default=PaymentChoices.card,
                               choices=PaymentChoices.choices, verbose_name=_("оплата"))
    city = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("город"))
    address = models.CharField(null=True, blank=True, max_length=50, verbose_name=_("адрес"))
    paid = models.BooleanField(default=False, verbose_name=_("оплачен заказ"))
    cost_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=_("стоимость доставки")
    )
    order_in = models.BooleanField(default=False, verbose_name=_("в заказе"))
    ordered = models.DateTimeField(null=True, blank=True, verbose_name=_("время заказа"))

    def __str__(self):
        return f"Заказ №{self.id}"

    def __len__(self):
        return len(self.order_goods.all())

    def get_absolute_url(self):
        return reverse("one-order", args=[str(self.id)])

    @property
    def all_goods_price_old(self):
        sum = 0
        for good in self.order_goods.all():
            sum += good.amount * good.old_price
        return sum

    @property
    def all_goods_price_new(self):
        sum = decimal.Decimal(0.00)
        for good in self.order_goods.all():
            sum += good.amount * good.price
        return sum

    @property
    def delivery_cost(self):
        if self.delivery == "экспресс":
            self.cost_delivery = decimal.Decimal(self.all_goods_price_new * decimal.Decimal(0.20)).quantize(
                decimal.Decimal("1.00")
            )
            return self.cost_delivery
        else:
            if self.all_goods_price_new > decimal.Decimal(100.00):
                self.cost_delivery = decimal.Decimal(self.all_goods_price_new * decimal.Decimal(0.03)).quantize(
                    decimal.Decimal("1.00")
                )
                return self.cost_delivery
            else:
                self.cost_delivery = decimal.Decimal(0.00)
                return self.cost_delivery

    @property
    def all_goods_price_disc_delivery(self):
        return decimal.Decimal(self.all_goods_price_new) + decimal.Decimal(self.delivery_cost)

    class Meta:
        ordering = ["-ordered"]
        verbose_name = _("заказ")
        verbose_name_plural = _("заказы")


class OrderGood(models.Model):
    good_in_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_goods", verbose_name=_("продукт в заказе")
    )
    good_in_cart = models.ForeignKey(
        Product,
        default=None,
        on_delete=models.CASCADE,
        related_name="order_goods",
        verbose_name=_("продукт в корзине"),
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("конечная цена"))
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("конечная цена"))
    amount = models.PositiveIntegerField(default=0, verbose_name=_("количество"))

    def __str__(self):
        return f"Продукт в заказе №{self.id} в количестве {self.amount}"

    class Meta:
        verbose_name = _("продукт в заказе")
        verbose_name_plural = _("продукты в заказе")
