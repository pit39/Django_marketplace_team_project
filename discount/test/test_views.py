from discount.test.base_test import BaseTest


class DiscountListTest(BaseTest):
    """Тесты списка скидок"""
    def test_discounts_list_view(self):
        response = self.client.get(self.discounts_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discount/discounts.html')

    def test_discount_on_list(self):
        response = self.client.get(self.discounts_list_url)
        self.assertContains(response, self.product_discount.title)

    def test_outdated_not_on_list(self):
        response = self.client.get(self.discounts_list_url)
        self.assertNotContains(response, self.outdated_discount.title)


class DiscountViewsTest(BaseTest):
    """Тесты детальных представлений скидок"""
    def test_product_discount_view(self):
        response = self.client.get(self.product_discount_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discount/product_discount.html')

    def test_data_on_product_discount_view(self):
        response = self.client.get(self.product_discount_url)
        self.assertContains(response, self.product_1.name)

    def test_pack_discount_view(self):
        response = self.client.get(self.pack_discount_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discount/pack_discount.html')

    def test_data_on_pack_discount_view(self):
        response = self.client.get(self.pack_discount_url)
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)

    def test_cart_discount_view(self):
        response = self.client.get(self.cart_discount_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discount/cart_discount.html')

    def test_data_on_cart_discount_view(self):
        response = self.client.get(self.cart_discount_url)
        self.assertContains(response, self.cart_discount.title)
