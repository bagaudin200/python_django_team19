import random

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from app_cart.models import ProductInCart, Cart
from app_order.models import Order
from app_payment.models import Payment
from .utils import card_number_is_valid


class PaymentService:
    """Сервис оплаты заказа"""

    def __init__(self, order_id, card_number, total_price):
        self.order_id = order_id
        self.card_number = str(card_number)
        self.total_price = total_price

    @transaction.atomic
    def pay(self):
        order = self._get_order()
        if isinstance(order, str):
            return order

        payment = Payment(order=order)
        if card_number_is_valid(self.card_number):
            cart = order.cart
            update_products = self._update_products_in_cart(cart)
            if update_products is True:
                order.status = self._get_random_success_status()
                order.save()
                cart.is_active = False
                cart.save()
                payment.save()
                return (f"OK: Payment for order #{self.order_id} from card {self.card_number} "
                        f"in the amount of ${self.total_price}")
            else:
                order.status = Order.STATUS_NOT_PAID
                order.save()
                reason = self._get_random_reason()
                payment.reason_for_non_payment = reason
                payment.save()
                return (f"ERROR: Order payment failed #{self.order_id} from card {self.card_number} "
                        f"in the amount of ${self.total_price}. "
                        f"Reason: {Payment.REASON_OUT_OF_STOCK}(product: {update_products}, "
                        f"requested: {update_products.quantity}, in stock: {update_products.product.quantity})")

        order.status = Order.STATUS_NOT_PAID
        order.save()

        reason = self._get_random_reason()
        payment.reason_for_non_payment = reason
        payment.save()
        return (f"ERROR: Order payment failed #{self.order_id} from card {self.card_number} "
                f"in the amount of ${self.total_price}. Reason: {reason}")

    def get_status(self) -> str:
        return self._get_order().status

    def _get_random_reason(self) -> str:
        return random.choice(
            [
                Payment.REASON_INSUFFICIENT_FUNDS,
                Payment.REASON_NO_CONTACT_WITH_BANK,
                Payment.REASON_CARD_BLOCKED
            ]
        )

    def _get_random_success_status(self) -> str:
        return random.choice(
            [Order.STATUS_OK, Order.STATUS_DELIVERED, Order.STATUS_PAID]
        )

    def _get_order(self):
        try:
            return Order.objects.get(id=self.order_id)
        except ObjectDoesNotExist:
            return f"ERROR: Order does not exist. Please place an order first"

    def _update_products_in_cart(self, cart: Cart):
        products_in_cart = ProductInCart.objects.filter(cart=cart)
        for item in products_in_cart:
            expected_quantity = item.product.quantity - item.quantity
            if expected_quantity < 0:
                return item
            item.product.quantity -= item.quantity
            item.product.sales_count += item.quantity
            item.product.save()
        return True
