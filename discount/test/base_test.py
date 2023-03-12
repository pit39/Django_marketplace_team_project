from typing import Union, Type
from django.test import TestCase
from django.urls import reverse

from fixtures.test_services.services import create_user, create_shop
from product.models import Product
from category.models import Category
from discount.models import ProductDiscount, DiscountedProduct, PackDiscount, CartDiscount, DiscountedPackProduct
import tempfile
from django.utils import timezone
from shop.models import Shop, ShopProduct


def create_some_product(suffix: str, category: Category) -> Product:
    product = Product.objects.create(name=f'testproduct{suffix}', category=category)
    return product


def create_discount(title: str, priority: int,
                    discount_model: Union[Type[ProductDiscount], Type[PackDiscount], Type[CartDiscount]],
                    cart_discount: bool = False) -> Union[ProductDiscount, PackDiscount, CartDiscount]:
    """Создает скидку по переданным параметрам"""
    discount = discount_model()
    discount.title = title
    discount.description = 'descr'
    discount.type = 'percent'
    discount.value = 50
    discount.priority = priority
    discount.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    if cart_discount:
        discount.condition = 'amount'
        discount.condition_min_value = 1
        discount.condition_max_value = 2
    discount.save()
    return discount


def add_products_to_product_discount(product: Product, discount: ProductDiscount) -> None:
    """Добавляет продукт к скидке на продукт"""
    DiscountedProduct.objects.create(discount=discount, product=product)


def add_products_to_pack_discount(product: Product, discount: PackDiscount, group: int) -> None:
    """Добавляет продукт к скидке на набор"""
    DiscountedPackProduct.objects.create(discount=discount, product=product, group=group)


def create_shop_product(shop: Shop, product: Product, price: int) -> ShopProduct:
    """Создает продукт продавца"""
    return ShopProduct.objects.create(store=shop, product=product, price=price, old_price=2, amount=1)


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='testcat', image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        category_2 = Category.objects.create(name='testcat_2', image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        product_1 = create_some_product('1', category)
        product_2 = create_some_product('2', category)
        product_3 = create_some_product('3', category)
        product_4 = create_some_product('4', category_2)
        product_discount = create_discount('test-product', 10, ProductDiscount)
        add_products_to_product_discount(product_1, product_discount)
        outdated_discount = create_discount('outdated_test_discount', 10, ProductDiscount)
        outdated_discount.end = timezone.now() - timezone.timedelta(1)
        outdated_discount.save()
        pack_discount = create_discount('test_pack_discount', 15, PackDiscount)
        add_products_to_pack_discount(product_1, pack_discount, group=1)
        add_products_to_pack_discount(product_2, pack_discount, group=2)
        add_products_to_pack_discount(product_3, pack_discount, group=2)
        cart_discount = create_discount('test_cart_discount', 20, CartDiscount, cart_discount=True)
        user = create_user()
        shop = create_shop(user)
        shop_product_1 = create_shop_product(shop, product_1, 200)
        shop_product_2 = create_shop_product(shop, product_2, 300)
        shop_product_3 = create_shop_product(shop, product_3, 200)
        invalid_discount = create_discount('invalid_test_pack_discount', 10, PackDiscount)
        add_products_to_pack_discount(product_1, invalid_discount, group=1)
        cls.product_4 = product_4
        cls.category = category
        cls.shop_product_1 = shop_product_1
        cls.shop_product_2 = shop_product_2
        cls.shop_product_3 = shop_product_3
        cls.invalid_discount = invalid_discount
        cls.user = user
        cls.product_1 = product_1
        cls.product_2 = product_2
        cls.product_3 = product_3
        cls.pack_discount = pack_discount
        cls.cart_discount = cart_discount
        cls.outdated_discount = outdated_discount
        cls.product_discount = product_discount
        cls.discounts_list_url = reverse('discounts')
        cls.product_discount_url = reverse('product-discount', kwargs={'pk': product_discount.id})
        cls.pack_discount_url = reverse('pack-discount', kwargs={'pk': pack_discount.id})
        cls.cart_discount_url = reverse('cart-discount', kwargs={'pk': cart_discount.id})
