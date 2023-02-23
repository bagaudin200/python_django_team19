from typing import List
from decimal import Decimal
from django.db.models import QuerySet, Min, Max
from app_settings.models import SiteSettings
from app_goods.models import Product


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


def get_cheapest_product_price(products: QuerySet) -> Decimal:
    """
    Возвращает цену самого дешевого товара
    :param products: список товаров
    :type products: QuerySet
    :return: цена самого дешевого товара
    :rtype: Decimal
    """
    return products.aggregate(price=Min('price'))['price']


def get_most_expensive_product_price(products: QuerySet) -> Decimal:
    """
    Возвращает цену самого дорогого товара
    :param products: список товаров
    :type products: QuerySet
    :return: цена самого дорогого товара
    :rtype: Decimal
    """
    return products.aggregate(price=Max('price'))['price']


def get_top_products(products: QuerySet) -> Product:
    """
    Возвращает самые популярные товары
    :param products:
    :return: самые популярные товары
    """
    quantity = SiteSettings.load()
    return products.prefetch_related('order_items').filter(available=True).only('category', 'name', 'price').annotate(total=Sum('order_items__quantity')).order_by('-total')[:quantity.top_items_count]


def get_limited_product(is_limited: QuerySet) -> Product:
    """
    Возвращает топ ограниченных товаров
    :param is_limited:
    :return: топ ограниченных товаров
    """
    return is_limited.select_related('category').filter(available=True).filter(limited=True). only('category', 'name', 'price')