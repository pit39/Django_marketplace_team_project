from django.test import TestCase

from payment.services import check_cart_number


class CheckCartNumberTest(TestCase):

    def test_valid_number(self):
        result = check_cart_number(card_number=10203044)
        self.assertTrue(result)

    def test_invalid_number(self):
        result = check_cart_number(card_number=10203040)
        self.assertFalse(result)

        result = check_cart_number(card_number=10203041)
        self.assertFalse(result)

        result = check_cart_number(card_number='1020304056')
        self.assertFalse(result)

        result = check_cart_number(card_number='10203040')
        self.assertFalse(result)
