from decimal import Decimal
from django.db.models import Q, QuerySet, Avg
from django.utils import timezone
from product.models import Product
from cart.services import Cart
from .models import DiscountedPackProduct, DiscountedPackCategory, PackDiscount, CartDiscount, ProductDiscount
from random import choice
from itertools import chain
from typing import List, Tuple, Union, Type
from shop.models import ShopProduct


def check_valid_pack_discount(obj: PackDiscount) -> bool:
    """Проверяет, добавлены ли к указанной скидке на набор товары или категории обеих групп """
    if (obj.products.filter(pack_discounts__group=1).exists() or
        obj.categories.filter(pack_discounts__group=1).exists()) and \
            (obj.products.filter(pack_discounts__group=2).exists() or
             obj.categories.filter(pack_discounts__group=2).exists()):
        return True
    else:
        return False


def get_discounts_queryset(discounts_model: Union[Type[ProductDiscount],
                                                  Type[PackDiscount], Type[CartDiscount]]) -> QuerySet:
    """Возвращает Queryset активных непросроченных скидок"""

    discounts = discounts_model.objects.filter(
        (Q(start__lte=timezone.now()) & Q(end__gte=timezone.now())) |
        (Q(start__lte=timezone.now()) & Q(end=None)) |
        (Q(start=None) & Q(end__gte=timezone.now())) |
        (Q(end=None) & Q(start=None)), active=True)
    return discounts


def check_pack_discount(discount: PackDiscount, cart: Cart) -> Union[Tuple[int, int], bool]:
    """Проверяет скидку на набор по корзине, если есть элементы и певрой и второй группы,
    возвращает по одному элементу из группы, или False, если скидка неприменима"""
    products = [product['shop_product'].product for product in cart]

    products_group_1 = DiscountedPackProduct.objects.filter(
        product__in=products, discount=discount, group=1).values_list('product_id')
    products_group_2 = DiscountedPackProduct.objects.filter(
        product__in=products, discount=discount, group=2).values_list('product_id')
    categories_group_1 = DiscountedPackCategory.objects.filter(
        category__products__in=products, discount=discount, group=1).values_list('category_id')
    categories_group_2 = DiscountedPackCategory.objects.filter(
        category__products__in=products, discount=discount, group=2).values_list('category_id')

    group_1 = [product[0] for product in products_group_1]
    group_1 += [product.id for product in products
                if product.category in categories_group_1 and product not in group_1]

    group_2 = [product[0] for product in products_group_2]
    group_2 += [product.id for product in products
                if product.category in categories_group_2 and product not in group_2]

    if len(group_1) > 0 and len(group_2) > 0:
        return choice(group_1), choice(group_2)
    else:
        return False


def check_cart_discount(discount: CartDiscount, cart: Cart) -> bool:
    """Проверяет скидку на корзину по корзине"""
    if discount.condition == 'amount':
        cart_len = len(cart)
        if discount.condition_min_value <= cart_len <= discount.condition_max_value:
            return True
    else:
        cart_price = cart.get_total_price()
        if discount.condition_min_value <= cart_price <= discount.condition_max_value:
            return True
    return False


def get_discount_for_cart(cart: Cart) \
        -> Union[Tuple[str, PackDiscount, Tuple[int, int]], Tuple[str, CartDiscount], bool]:
    """Проверяет скидки на корзины и наборы по корзине, начиная с самой приоритетной,
    возвращает тип скидки, скидку, и товары на которые устанавливается скидка, если это набор"""
    products = [product['shop_product'].product for product in cart]

    cart_discount = get_discounts_queryset(CartDiscount).filter(
        Q(condition='amount') & Q(condition_min_value__lte=len(cart)) & Q(condition_max_value__gte=len(cart)) |
        Q(condition='sum') & Q(condition_min_value__lte=cart.get_total_price()) &
        Q(condition_max_value__gte=cart.get_total_price())).order_by('-priority')

    pack_discounts = get_discounts_queryset(PackDiscount).filter(
        Q(products__in=products) | Q(categories__products__in=products)).distinct()

    discount_list = list(chain(cart_discount, pack_discounts))
    discount_list.sort(key=lambda x: x.priority, reverse=True)
    for discount in discount_list:
        if isinstance(discount, PackDiscount):
            valid_discount = check_pack_discount(discount, cart)
            if valid_discount:
                return 'pack', discount, valid_discount
        else:
            return 'cart', discount
    return False


def get_all_product_discounts(product: Product) -> QuerySet:
    """Возвращает список всех доступных скидок для продукта"""
    discounts = get_discounts_queryset(ProductDiscount).filter(
        Q(products=product) | Q(categories__products=product)).distinct()
    return discounts


def get_product_discount(product: Product) -> ProductDiscount:
    """Возвращает приоритетную скидку на продукт"""
    discount = get_all_product_discounts(product).order_by('-priority').first()
    return discount


def get_all_discounts(*products: Product) -> QuerySet:
    """ Возвращает список доступных скидок для списка продуктов """
    discounts = get_discounts_queryset(ProductDiscount).filter(
        Q(products__in=products) | Q(categories__products__in=products)).distinct()
    return discounts


def get_priority_discounts(*products: Product) -> Union[List[Tuple[Product, ProductDiscount]], bool]:
    """Возвращает список кортежей из продукта и наиболее приоритетной скидки из переданного списка продуктов"""
    discount_list = []
    for product in products:
        discount = get_product_discount(product)
        if discount:
            discount_list.append((product, discount))
    if len(discount_list) > 0:
        return discount_list
    else:
        return False


def calculate_discount(
        price: Union[Decimal, int], discount: Union[ProductDiscount, PackDiscount, CartDiscount]) -> Decimal:
    """Принимает цену и скидку, возвращает цену со скидкой"""
    if discount.type == 'percent':
        discounted_price = price - price / 100 * discount.value
    elif discount.type == 'sum':
        discounted_price = price - discount.value
    else:
        discounted_price = discount.value
    if discounted_price < 1:
        discounted_price = Decimal('1')
    return discounted_price


def get_discounted_price(product: Product, discount: Union[ProductDiscount, PackDiscount],
                         price: Union[Decimal, int] = None) -> Decimal:
    """Возвращает рассчитанную цену со скидкой на продукт, если передана цена, то на ее основе,
    если нет, то берет среднюю цену на продукт"""
    if not price:
        price = ShopProduct.objects.filter(product=product).aggregate(Avg('price'))['price__avg']
    discounted_price = calculate_discount(price, discount)
    return discounted_price
