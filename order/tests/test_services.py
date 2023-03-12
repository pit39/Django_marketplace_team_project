from django.test import TestCase

from order.models import Order
from order.services import PaymentService
from payment.models import PaymentInfo, ErrorMessage
from fixtures.test_services.services import create_user, create_shop_product, create_shop, create_product, \
    create_order, create_order_good, create_payment_info, add_product_in_cart


def get_payment_info() -> PaymentInfo:
    user = create_user()
    order = create_order(user)
    good = create_shop_product(create_shop(user), create_product())
    good_in_cart = add_product_in_cart(user=user, product=good)
    create_order_good(order=order, good=good_in_cart)
    return create_payment_info(order)


class TestPaymentService(TestCase):

    def setUp(self):
        self.payment_info = get_payment_info()

    def test_update_after_success_pay_func(self):
        """
        Тест проверяет удаление из БД платежной информации и выставление статуса оплачен заказу при успешной оплате
        """
        self.payment_info.status = 'f'
        ErrorMessage.objects.create(payment_info=self.payment_info, message='test')
        PaymentService.update_after_success_pay(payment_info=self.payment_info)

        self.assertEqual(ErrorMessage.objects.count(), 0)
        self.assertEqual(PaymentInfo.objects.count(), 0)
        self.assertTrue(Order.objects.first().paid)

    def test_update_after_fail_pay(self):
        """Тест проверяет смену статуса оплаты заказа и добавление сообщения об ошибке при неудачной оплате"""
        ErrorMessage.objects.create(payment_info=self.payment_info, message='start_error_message')
        PaymentService.update_after_fail_pay(payment_info=self.payment_info, error_message='test')

        self.assertEqual(PaymentInfo.objects.count(), 1)
        self.assertEqual(PaymentInfo.objects.first().status, 'f')

        self.assertFalse(Order.objects.first().paid)

        self.assertEqual(ErrorMessage.objects.count(), 1)
        self.assertEqual(ErrorMessage.objects.first().message, 'test')
