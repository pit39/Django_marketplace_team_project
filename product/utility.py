from django.db.models import Avg, Min, Max


class ProductRatingMixin:
    """Класс миксин. Добавляет метод дечернему классу."""

    @property
    def rating(self) -> int:
        return self.reviews.aggregate(Avg('rating')).get('rating__avg')


class ProductPriceMixin:
    """Класс миксин. Добавляет метод дечернему классу."""

    @property
    def price(self):
        return self.shop_products.aggregate(Min('price')).get('price__min')

    @property
    def old_price(self):
        return self.shop_products.aggregate(Max('old_price')).get('old_price__max')


class ProductDiscountMixin:
    @property
    def discount(self):
        """Отображает приоритетную скидку на продукт в текстовом варианте,
        в зависимости от механизма рассчета скидки"""
        discount_display = None
        from discount.services import get_product_discount
        discount = get_product_discount(self)
        if discount:
            if discount.type == 'percent':
                discount_display = f'-{int(discount.value)}%'
            elif discount.type == 'sum':
                discount_display = f'-{int(discount.value)}'
            else:
                discount_display = int(discount.value)

        return discount_display
