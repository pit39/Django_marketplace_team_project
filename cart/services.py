import random
from typing import Optional
from decimal import Decimal

from django.http import Http404
from django.shortcuts import get_object_or_404

from product.models import Product
from shop.models import ShopProduct
from cart.models import ProductInCart
from cart.forms import CartAddProductForm
from config.settings.base import CART_SESSION_ID


class Cart(object):
    """Класс, описывающий корзину пользователя"""
    EXCLUDE_FIELDS = ('store__description', 'store__slug', 'store__address', 'store__email', 'store__phone', 'amount',
                      'product__category_id', 'product__created_at', 'product__views', 'product__updated_at',
                      'store__holder_id', 'store__logo',
                      )

    def __init__(self, request) -> None:
        """Инициализируем корзину"""
        self.user = request.user
        self.auth = self.user.is_authenticated
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.get_cart_for_auth_user() if self.auth else {}
            self.session[CART_SESSION_ID] = cart

        self.cart = cart

    def get_cart_for_auth_user(self) -> dict:
        """Функция возвращает корзину авторизованного пользователя для сессий"""
        cart = {}
        queryset = ProductInCart.objects.filter(user=self.user).select_related('shop_product__product')

        for cart_item in queryset:
            shop_product = cart_item.shop_product
            cart[str(shop_product.product.id)] = {
                    'shop_product_id': shop_product.id,
                    'price': str(shop_product.price),
                    'quantity': cart_item.quantity
            }

        return cart

    def check_product_before_ad(self, shop_product: ShopProduct, quantity: int = 1) -> None:
        """Функция проверяет есть ли товар в корзине и либо обновляет его кол-во, либо добавляет"""
        shop_product_id = shop_product.id
        product_id = str(shop_product.product.id)

        if self.product_in_session_cart(product_id, shop_product_id) and self.product_in_user_cart(shop_product_id):
            self.update(shop_product, quantity, True)
        else:
            self.add(shop_product, quantity)

    def product_in_session_cart(self, product_id: str, shop_product_id: int) -> bool:
        """Функция проверяет, что товар с нужным продавцом есть в корзине для неавторизованного пользователя"""
        return product_id in self.cart and self.cart[product_id]['shop_product_id'] == shop_product_id

    def product_in_user_cart(self, shop_product_id: int) -> bool:
        """Функция проверяет, что товар с нужным продавцом есть в корзине для авторизованного пользователя"""
        return not self.auth or ProductInCart.objects.filter(user=self.user, shop_product_id=shop_product_id).exists()

    def add(self, shop_product: ShopProduct, quantity: int = 1) -> None:
        """Метод добавления товара в корзину"""
        shop_product_id = shop_product.id
        product_id = str(shop_product.product.id)

        self.cart[product_id] = {
            'shop_product_id': shop_product_id,
            'price': str(shop_product.price),
            'quantity': quantity
        }
        self.save()

        if self.auth:
            (ProductInCart.objects
                          .update_or_create(
                              user=self.user,
                              shop_product__product_id=product_id,
                              defaults={'shop_product': shop_product, 'quantity': quantity}
                          ))

    def update(self, shop_product: ShopProduct, quantity: int, in_cart: bool = False) -> None:
        """Метод изменения кол-ва товара в корзине"""
        product_id = str(shop_product.product.id)

        if not in_cart:
            if product_id not in self.cart:
                raise Http404

        self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product_id)

        else:
            self.save()
            if self.auth:
                try:
                    user_cart_product = ProductInCart.objects.only('quantity').get(
                        user=self.user,
                        shop_product=shop_product
                    )
                    user_cart_product.quantity += quantity
                    user_cart_product.save(update_fields=['quantity'])

                except ProductInCart.DoesNotExist:
                    raise Http404

    def save(self) -> None:
        """Обновляет состояние корзины"""
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id: str) -> None:
        """Удаление товара из корзины"""
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

        if self.auth:
            cart_product = get_object_or_404(klass=ProductInCart, user=self.user, shop_product__product_id=product_id)
            cart_product.delete()

    def __iter__(self) -> dict:
        """Перебор элементов в корзине"""
        shop_product_ids = [values['shop_product_id'] for values in self.cart.values()]

        shop_products = (ShopProduct.objects
                         .filter(id__in=shop_product_ids)
                         .select_related('store', 'product')
                         .prefetch_related('product__shop_products__product__images')
                         .defer(*self.EXCLUDE_FIELDS))

        cart = self.cart.copy()
        for shop_product in shop_products:
            cart[str(shop_product.product.id)]['shop_product'] = shop_product

        for item in cart.values():
            yield item

    def __len__(self) -> int:
        """Подсчет всех товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> int:
        """Подсчет стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self) -> None:
        """Удаление корзины из БД"""
        if self.auth:
            for key, item in self.cart.items():
                ProductInCart.objects.get(shop_product=item['shop_product_id'], user=self.user).delete()

        del self.session[CART_SESSION_ID]
        self.session.modified = True


def get_product(pk: int, *args) -> Product:
    """Возвращает товар"""
    try:
        return Product.objects.only(*args).get(id=pk)
    except Product.DoesNotExist:
        raise Http404


def get_shop_product(pk: int, *args) -> ShopProduct:
    """Возвращает магазин"""
    try:
        return ShopProduct.objects.only(*args).get(id=pk)
    except ShopProduct.DoesNotExist:
        raise Http404


def get_random_shop_product(product_id: int, *args) -> ShopProduct:
    """Возвращает случайный магазин для товара"""
    return random.choice(ShopProduct.objects.all().only(*args).filter(product_id=product_id))


def get_form_add_cart(request) -> Optional[CartAddProductForm]:
    """Возвращает форму с кол-вом товара, если был сделан post запрос"""
    form = None
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)

    return form


def add_product_to_cart(request, product_pk: int, shop_product_pk: Optional[int], form=None) -> None:
    """Добавляет товар в корзину"""
    cart = Cart(request)
    shop_product = get_shop_product(shop_product_pk) if shop_product_pk else get_random_shop_product(product_pk)

    data_for_add = {'shop_product': shop_product}
    if form:
        data = form.cleaned_data
        data_for_add['quantity'] = data['quantity']

    cart.check_product_before_ad(**data_for_add)


def change_count_cart(request, shop_product_pk, quantity) -> None:
    """Изменяет кол-во товара в корзине"""
    cart = Cart(request)
    shop_product = get_shop_product(shop_product_pk)
    cart.update(shop_product, quantity)


def remove_product(request, pk: int) -> None:
    """Удаляет товар из корзины"""
    cart = Cart(request)
    cart.remove(str(pk))
