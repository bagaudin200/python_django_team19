from decimal import Decimal
from typing import Tuple, Any

from django.db.models import Sum, F, QuerySet

from app_cart.services import CartServices
from app_order.models import Order
from app_settings.models import SiteSettings


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, request):
        self.request = request
        self.cart = CartServices(request).cart

    def get_last_order(self) -> Order:
        """
        Возвращает последнюю заказ пользователя
        :return: последнюю заказ пользователя
        """
        return Order.objects.select_related('cart__user').filter(cart__user=self.cart.user).last()

    def get_order_by_id(self, id_: int) -> Order:
        """
        Возвращает заказ по id
        :return: заказ пользователя
        """
        return Order.objects.get(id=id_)

    def get_history(self) -> QuerySet[Order]:
        """
        Возвращает историю заказов
        :return: история заказов
        """
        return Order.objects.select_related('cart__user').filter(cart__user=self.cart.user).order_by('-created_at')

    def paid(self, order) -> bool:
        """
        Возвращает статус заказа
        :param order: модель заказа
        :return: булево значение
        """
        return order.status in [Order.STATUS_OK, Order.STATUS_PAID, Order.STATUS_DELIVERED]

    def get_status(self) -> str:
        """
        Получение статуса заказа
        :return: статус заказа
        """
        return 'Оплачено'

    def get_info_about_delivery_and_payment(self) -> Tuple[Any, Any]:
        """
        Получение информации из сессии о типе доставки и оплаты
        :return: имя типа доставки и имя типа оплаты заказа
        """
        delivery_name = Order.DELIVERY_TYPES_DICT.get(self.request.session['delivery'])
        payment_name = Order.PAYMENT_TYPES_DICT.get(self.request.session['payment'])
        return delivery_name, payment_name

    def get_total_price(self):
        """
        Получение стоимости заказа с учетом выбранного типа доставки
        :return: стоимость заказа
        """
        total_price = self.cart.products.only('quantity', 'price').aggregate(total=Sum(F('quantity') *
                                                                                       F('product__price')))['total']
        if total_price < SiteSettings.load().min_order_price_for_free_shipping:
            total_price += Decimal(SiteSettings.load().standard_order_price)
        if self.request.session.get('delivery') == 'express':
            total_price += Decimal(SiteSettings.load().express_order_price)
        return total_price

    def get_format_phone_number(self) -> str:
        """
        Получение отформатированного номера телефона
        :return: отформатированный номер телефона
        """
        if self.request.user.phoneNumber:
            phone_number = '+7 ({}{}{}) {}{}{}-{}{}-{}{}'.format(
                self.request.user.phoneNumber[0],
                self.request.user.phoneNumber[1],
                self.request.user.phoneNumber[2],
                self.request.user.phoneNumber[3],
                self.request.user.phoneNumber[4],
                self.request.user.phoneNumber[5],
                self.request.user.phoneNumber[6],
                self.request.user.phoneNumber[7],
                self.request.user.phoneNumber[8],
                self.request.user.phoneNumber[9],
            )
            return phone_number
        else:
            return ''
