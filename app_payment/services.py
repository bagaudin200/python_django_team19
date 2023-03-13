from django.core.exceptions import ObjectDoesNotExist

from app_order.models import Order
from .utils import card_number_is_valid


class PaymentService:
    def __init__(self, order_id, card_number, total_price):
        self.order_id = order_id
        self.card_number = str(card_number)
        self.total_price = total_price

    def pay(self):
        order = self._get_order()
        if isinstance(order, str):
            return order
        if card_number_is_valid(self.card_number):
            order.status = Order.STATUS_OK
            order.save()

            return f"OK: Payment for order #{self.order_id} from card {self.card_number} in the amount of ${self.total_price}"

        order.status = Order.STATUS_INVALID_CARD_NUMBER
        order.save()
        return f"ERROR: Order payment failed #{self.order_id} from card {self.card_number} in the amount of ${self.total_price}. Cause: {order.status}"

    def get_status(self):
        return self._get_order().status

    def _get_order(self):
        try:
            return Order.objects.get(id=self.order_id)
        except ObjectDoesNotExist:
            return f"ERROR: Order does not exist. Please place an order first"

