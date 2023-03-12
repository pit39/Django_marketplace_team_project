from django.test import TestCase
from django.urls import reverse


class PaymentAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        valid_kvargs = {'card_number': 20304056, 'cost': 2000}
        invalid_kvargs = {'card_number': 2030405060, 'cost': 2000}

        cls.valid_page_name = reverse(viewname='payment:pay', kwargs=valid_kvargs)
        cls.invalid_page_name = reverse(viewname='payment:pay', kwargs=invalid_kvargs)

    def test_valid_pay(self):
        """Тест оплаты с валидным номером карты"""
        response = self.client.get(self.valid_page_name)
        self.assertEqual(response.status_code, 201)

    def test_invalid_pay(self):
        """Тест оплаты с не валидным номером карты"""
        response = self.client.get(self.invalid_page_name)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
