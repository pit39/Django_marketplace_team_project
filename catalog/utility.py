from typing import Optional
from django.db.models import Min
from product.models import Product


class CatalogMixin:

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category').prefetch_related('property')
        return queryset


class CatalogOrderByMixin:

    field: Optional[str] = None

    def get_queryset(self):

        if '__' in self.field:
            queryset = super().\
                get_queryset().annotate(Min(self.field)).order_by('{}__min'.format(self.switched_field()))
        else:
            queryset = super().get_queryset().order_by(self.switched_field())
        return queryset

    def switched_field(self):
        get_args = [self.request.GET.get(_) for _ in ('page', 'query', 'price', 'title', 'is_exist', 'seller')]
        reverse = self.request.session.get('reverse', '') if not any(get_args) else self.request.session['unreverse']
        field = reverse + self.field

        if reverse is None and not any(get_args):
            self.request.session['reverse'] = ''
            self.request.session['unreverse'] = '-'

        elif reverse == '' and not any(get_args):
            self.request.session['reverse'] = '-'
            self.request.session['unreverse'] = ''

        elif reverse == '-' and not any(get_args):
            self.request.session['reverse'] = ''
            self.request.session['unreverse'] = '-'
        return field


class SearchMixin:

    def get_queryset(self):
        queryset = super().get_queryset().filter(name__contains=self.request.GET.get('query', ''))
        return queryset


class FilterMixin:

    def get_queryset(self):
        if any(self.filters().values()):
            queryset = super().get_queryset().filter(**self.filters())
        else:
            queryset = super().get_queryset()
        return queryset

    @classmethod
    def clean_value(cls, key: str, value: str):
        if key == 'price':
            price_from, price_to = value.split(';')
            return {'price_from': int(price_from), 'price_to': int(price_to)}
        return value

    def get_data_filter(self) -> dict:
        return {
            key: self.clean_value(key, value) for key, value in self.request.GET.items() if value
        }

    def is_exist(self) -> int:
        is_exist: Optional[str] = self.get_data_filter().get('is_exist')
        result: int = 0
        if is_exist and is_exist == 'on':
            result = 1
        return result

    def filters(self) -> dict:
        data: dict = self.get_data_filter()
        return {
            'shop_products__price__gte': data.get('price', dict()).get('price_from'),
            'shop_products__price__lte': data.get('price', dict()).get('price_to'),
            'shop_products__product__name__icontains': data.get('title', ''),
            'shop_products__amount__gte': self.is_exist(),
        } | ({'shop_products__store__pk': data.get('seller')} if data.get('seller') else dict())


class FavouriteLowestPriceMixin:

    @property
    def lowest_price(self):
        lowest_price_aggregation = Product.objects.filter(
            category=self.category).aggregate(Min('shop_products__price'))
        lowest_price = lowest_price_aggregation['shop_products__price__min']
        return lowest_price
