from django.test import TestCase
from django.shortcuts import reverse
from fixtures.test_services.services import create_user, create_shop_product, create_shop, create_product


class OrderTest(TestCase):
    def setUp(self):
        self.user = create_user("user@user.user")
        self.customer = create_user("customer@customer.customer")
        self.product = create_product("product")
        create_shop_product(create_shop(self.customer), self.product)
        self.client.force_login(user=self.user)
        self.client.get(reverse("cart:random_add", kwargs={"product_pk": 1}))
        self.client.post(
            "/order/step1/", {"email": "test@test.ru", "first_second_names": "Тест", "phone": "375299999999"}
        )
        self.client.post("/order/step2/", {"city": "Город", "address": "Адрес"})

    def test_order_with_credit_card(self):
        self.client.post("/order/step3/", {"payment": "random"})
        response = self.client.get("/order/step4/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test@test.ru")
        self.assertContains(response, "Тест")
        self.assertContains(response, "Онлайн со случайного чужого счёта")
        self.assertContains(response, "375299999999")
        self.assertContains(response, "1")
        self.assertContains(response, "2")

    def test_order_with_cash(self):
        self.client.post("/order/step3/", {"payment": "card"})
        response = self.client.get("/order/step4/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test@test.ru")
        self.assertContains(response, "Тест")
        self.assertContains(response, "Онлайн картой")
        self.assertContains(response, "375299999999")
        self.assertContains(response, "1")
        self.assertContains(response, "2")
        self.assertContains(response, "Оплата при получении")

    def test_history_order(self):
        response = self.client.get("/order/history/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Ваша история заказов")

    def test_history_detail_order(self):
        response = self.client.get("/order/history/1/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertContains(response, "2")
        self.assertContains(response, "Не оплачен")

    def test_page_payment_number_card(self):
        response = self.client.get("/order/payment/order/5/")
        self.assertContains(response, "Номер карты")
