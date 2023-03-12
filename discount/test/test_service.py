from cart.services import Cart
from discount.test.base_test import BaseTest, create_discount, add_products_to_product_discount
from discount.services import check_valid_pack_discount, get_discounts_queryset, check_pack_discount, \
    check_cart_discount, get_discount_for_cart, get_all_product_discounts, get_product_discount, get_all_discounts, \
    get_priority_discounts, calculate_discount, get_discounted_price
from discount.models import ProductDiscount, DiscountedCategory


class CheckValidPackDiscountTest(BaseTest):
    """Тесты проверки валидации скидок на набор"""

    def test_valid_discount(self):
        validate = check_valid_pack_discount(self.pack_discount)
        self.assertTrue(validate)

    def test_invalid_discount(self):
        validate = check_valid_pack_discount(self.invalid_discount)
        self.assertFalse(validate)


class GetDiscountsQuerysetTest(BaseTest):
    """Тесты выборки актуальных скидок"""
    def test_actual_discount(self):
        discounts = get_discounts_queryset(ProductDiscount)
        self.assertTrue(self.product_discount in discounts)

    def test_outdated_discount(self):
        discounts = get_discounts_queryset(ProductDiscount)
        self.assertFalse(self.outdated_discount in discounts)


class CheckPackDiscountTest(BaseTest):
    """Тесты основных сервисов работы со скидками"""
    def setUp(self) -> None:
        self.client.force_login(user=self.user)
        self.session = self.client.session
        self.cart = Cart(self)
        self.cart.add(self.shop_product_1, 1)
        self.cart.add(self.shop_product_2, 1)
        self.product_discount_2 = create_discount('test-product-2', 15, ProductDiscount)
        self.product_discount_3 = create_discount('test-product-3', 12, ProductDiscount)
        self.product_discount_4 = create_discount('test-product-4', 13, ProductDiscount)
        self.product_discount_5 = create_discount('test-product-5', 14, ProductDiscount)
        self.product_discount_6 = create_discount('test-product-6', 17, ProductDiscount)
        add_products_to_product_discount(self.product_1, self.product_discount_2)
        add_products_to_product_discount(self.product_1, self.product_discount_3)
        DiscountedCategory.objects.create(category=self.category, discount=self.product_discount_4)
        add_products_to_product_discount(self.product_3, self.product_discount_5)

    def test_check_pack_discount_valid(self):
        """Тест проверки применимой скидки на набор"""
        pass
        # check = check_pack_discount(self.pack_discount, self.cart)
        # self.assertEqual(check, (self.product_1.id, self.product_2.id))

    def test_check_pack_discount_invalid(self):
        """Тест проверки неприменимой скидки на набор"""
        self.cart.add(self.shop_product_3, 1)
        self.cart.remove(str(self.product_1.id))
        check = check_pack_discount(self.pack_discount, self.cart)
        self.assertFalse(check)

    def test_check_cart_discount_valid(self):
        """Тест проверки применимой скидки на корзину"""
        check = check_cart_discount(self.cart_discount, self.cart)
        self.assertTrue(check)

    def test_check_cart_discount_invalid(self):
        """Тест проверки неприменимой скидки на корзину"""
        self.cart.add(self.shop_product_3, 1)
        check = check_cart_discount(self.cart_discount, self.cart)
        self.assertFalse(check)

    def test_get_discount_for_cart_valid_high_priority(self):
        """Тест алгоритма поиска скидки для корзины, применима более приоритетная скидка """
        get_discount = get_discount_for_cart(self.cart)
        self.assertEqual(get_discount, ('cart', self.cart_discount))

    def test_get_discount_for_cart_valid_less_priority(self):
        """Тест алгоритма поиска скидки для корзины, применима менее приоритетная скидка """
        self.cart.add(self.shop_product_1, 5)
        get_discount = get_discount_for_cart(self.cart)
        self.assertEqual(get_discount, ('pack', self.pack_discount, (self.product_1.id, self.product_2.id)))

    def test_no_valid_discounts_for_cart(self):
        """Тест алгоритма поиска скидки для корзины, нет применимых скидок """
        self.cart.add(self.shop_product_1, 5)
        self.cart.remove(str(self.product_2.id))
        get_discount = get_discount_for_cart(self.cart)
        self.assertFalse(get_discount)

    def test_get_all_product_discounts(self):
        """Тест поиска всех скидок на продукт для продукта"""
        discounts = get_all_product_discounts(self.product_1)
        self.assertEqual(len(discounts), 4)

    def test_get_product_discount(self):
        """Тест поиска приоритетной скидки на продукт"""
        discount = get_product_discount(self.product_1)
        self.assertEqual(self.product_discount_2, discount)

    def test_get_all_discounts(self):
        """Тест поиска скидок для списка продутов"""
        discounts = get_all_discounts(self.product_1, self.product_2, self.product_3)
        self.assertEqual(len(discounts), 5)

    def test_get_priority_discounts(self):
        """Тест поиска приоритетных скидок для списка продуктов"""
        discount_list = get_priority_discounts(self.product_1, self.product_2, self.product_4)
        self.assertEqual(discount_list, [(self.product_1, self.product_discount_2),
                                         (self.product_2, self.product_discount_4)])

    def test_calculate_discount(self):
        """Тест рассчета цены по скидке"""
        discounted_price = calculate_discount(50, self.product_discount)
        self.assertEqual(discounted_price, 25)

    def test_get_discounted_price(self):
        """Тест рассчета цены для продукта без указания цены"""
        discounted_price = get_discounted_price(self.product_1, self.product_discount)
        self.assertEqual(discounted_price, 100)

    def test_get_discounted_price_with_price_set(self):
        """Тест рассчета цены для продукта с указанием цены"""
        discounted_price = get_discounted_price(self.product_1, self.product_discount, 500)
        self.assertEqual(discounted_price, 250)
