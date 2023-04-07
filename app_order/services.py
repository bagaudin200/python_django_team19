from typing import List

from django.db.models import Sum, F

from app_cart.models import Cart
from app_order.models import Order
from app_cart.services import CartServices
from app_settings.models import SiteSettings


class OrderService:
    """Сервис для работы с заказами"""
    def __init__(self, request):
        self.request = request
        self.cart = CartServices(request).cart
    def get_history(self) -> List:
        """
        Возвращает историю заказов пользователя
        :return: история заказов
        :rtype: list
        """
        return ['Товар 1', 'Товар 2', 'Товар 3']

    def payment(self) -> None:
        """
        Оплата заказа
        :return: None
        :rtype: None
        """
        pass

    def get_status(self) -> str:
        """
        Получение статуса заказа
        :return: статус заказа
        :rtype: str
        """
        return 'Оплачено'

    def get_info_about_delivery_and_payment(self):
        """Получение информации из сессии о типе доставки и оплаты"""
        delivery_name = Order.DELIVERY_TYPES_DICT.get(self.request.session['delivery'])
        payment_name = Order.PAYMENT_TYPES_DICT.get(self.request.session['payment'])
        return delivery_name, payment_name

    def get_total_price(self):
        """Получение информации об общей стоимости заказа"""
        total_price = self.cart.products.only('quantity', 'price').aggregate(total=Sum(F('quantity') *
                                                                                       F('product__price')))['total']
        if total_price < 100:
            total_price += SiteSettings.load().standard_order_price
        if self.request.session.get('delivery') == 'express':
            total_price += SiteSettings.load().express_order_price
        return total_price
        
    def get_format_phone_number(self):
        """Получение отформатированного номера телефона"""
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
