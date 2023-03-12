from django.views.generic import ListView, DetailView
from .models import CartDiscount, PackDiscount, ProductDiscount
from itertools import chain
from .services import get_discounts_queryset


class DiscountsView(ListView):
    paginate_by = 16
    template_name = 'discount/discounts.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        product_discounts = get_discounts_queryset(ProductDiscount)
        pack_discounts = get_discounts_queryset(PackDiscount)
        cart_discounts = get_discounts_queryset(CartDiscount)
        queryset = list(chain(product_discounts, pack_discounts, cart_discounts))
        return queryset


class ProductDiscountView(DetailView):
    model = ProductDiscount
    context_object_name = 'discount'
    template_name = 'discount/product_discount.html'


class PackDiscountView(DetailView):
    model = PackDiscount
    context_object_name = 'discount'
    template_name = 'discount/pack_discount.html'


class CartDiscountView(DetailView):
    model = CartDiscount
    context_object_name = 'discount'
    template_name = 'discount/cart_discount.html'
