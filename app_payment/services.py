from app_order.models import Order


class PaymentService:

    def __init__(self, order_id, card_number, total_price):
        self.order_id = order_id
        self.card_number = card_number
        self.total_price = total_price

    def pay(self):
        order = self._get_order()
        order.status = 'ok'

    def get_status(self):
        return self._get_order().status

    def _get_order(self):
        return Order.objects.get(id=self.order_id)
