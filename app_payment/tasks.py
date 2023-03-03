from config.celery import app
from app_order.models import Order
from .services import PaymentService


@app.task(name='pay')
def pay(order_id, card_number, total_price):
    """Задача оплаты заказа при его оформлении."""
    payment = PaymentService(order_id, card_number, total_price)
    payment.pay()
    return {'pay': 'ok'}
    