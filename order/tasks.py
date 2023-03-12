from celery import shared_task

from .services import PaymentService


@shared_task
def pay_for_orders() -> None:
    """Периодическая задача оплаты заказов"""
    orders_payment_info = PaymentService.get_wait_list()

    for order_payment_info in orders_payment_info:
        response = PaymentService.try_to_pay(payment_info=order_payment_info)

        PaymentService.update_payment_info(response, order_payment_info)
