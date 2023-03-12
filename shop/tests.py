from django.test import TestCase
from django.urls import reverse

from fixtures.test_services.services import create_user, create_product, create_shop_product, create_shop


class ShopTest(TestCase):
    def setUp(self):
        self.customer = create_user("customer@customer.customer")
        self.product = create_product("product")
        create_shop_product(create_shop(self.customer), self.product)
        self.client.force_login(user=self.customer)

    def test_create_shop_(self):
        response = self.client.get(reverse("create-shop"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Введите название")
        self.assertContains(response, "Выберите лого")
        self.assertContains(response, "Адрес")
        self.assertContains(response, "Телефон")

    def test_add_product_to_the_shop(self):
        response = self.client.get(reverse("create-good"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Добавление товара в магазин")
        self.assertContains(response, "Выберите магазин")
        self.assertContains(response, "Выберите продукт")
