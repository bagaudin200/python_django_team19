from config.celery import celery_app
from .services import PaymentService


@celery_app.task
def pay(order_id, card_number, total_price):
    """Задача оплаты заказа при его оформлении."""
    payment = PaymentService(order_id, card_number, total_price)
    payment.pay()
    return f"Прошла оплата заказа #{order_id} с номера карты {card_number} на сумму {total_price}"
