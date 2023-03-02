from typing import List
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import QuerySet, Min, Max
from app_cart.models import Cart
from app_goods.models import Product


user = get_user_model()


class ReviewService:
    """Сервис для работы с отзывами"""

    def __init__(self, profile: object):
        self.profile = profile

    def add(self, product: object, review: str) -> None:
        """
        Добавляет отзыв к товару
        :param product: товар
        :type product: object
        :param review: текст отзыва
        :type review: str
        :return: None
        :rtype: None
        """
        pass

    def get_reviews_for_product(self, product: object) -> List:
        """
        Возвращает список отзывов к товару
        :param product: товар
        :type product: object
        :return: список отзывов
        :rtype: list
        """
        return ['Отзыв1', 'Отзыв2', 'Отзыв3']

    def get_reviews_count(self, product: object) -> int:
        """
        Возвращает количество отзывов для товара
        :param product: товар
        :type product: object
        :return: количество отзывов для товара
        :rtype: int
        """
        return 3


def get_cheapest_product(products: QuerySet) -> Decimal:
    """
    Возвращает цену самого дешевого товара
    :param products: список товаров
    :type products: QuerySet
    :return: самый дешевый товар
    :rtype: Product
    """
    return products.aggregate(price=Min('price'))['price']


def get_most_expensive_product(products: QuerySet) -> Product:
    """
    Возвращает самый дорогой товар
    :param products: список товаров
    :type products: QuerySet
    :return: самый дорогой товар
    :rtype: Product
    """
    return products.aggregate(price=Max('price'))['price']


def get_update_quantity_product(product: Product, user: User) -> bool:
    """
    Возвращает булево значения, для добавление товара или обновления его количетсва в корзине
    """
    update_product = False
    if not user.is_anonymous:
        cart = Cart.objects.get(user=user, good=product)
        print('cart', cart)
        if cart:
            update_product = True
    else:
        pass
    return update_product


