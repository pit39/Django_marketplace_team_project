from django.shortcuts import redirect
from django.views.generic import TemplateView

from .services import add_product_to_cart, remove_product, get_form_add_cart, get_product, change_count_cart


class CartView(TemplateView):
    """Представление корзины пользователя"""
    template_name = 'cart.html'


def cart_add(request, product_pk, shop_product_pk=None):
    """Представление добавления товара в корзину"""
    product = get_product(product_pk, 'pk', 'slug')
    form = get_form_add_cart(request)

    if request.method == 'GET' or form.is_valid():
        add_product_to_cart(request, product_pk, shop_product_pk, form)
    return redirect(to='product', slug=product.slug)


def change_count(request, shop_product_pk, quantity):
    """Представления изменения кол-во товара в корзине"""
    change_count_cart(request, shop_product_pk, int(quantity))
    return redirect(to='cart:cart')


def cart_remove(request, pk: int):
    """Представление удаления товара из корзины"""
    remove_product(request, pk)
    return redirect(to='cart:cart')
