from typing import List

from django.contrib.auth import get_user_model

from app_cart.models import ProductInCart
from app_goods.models import Product, Review

user = get_user_model()


class ReviewService:
    """Сервис для работы с отзывами"""

    def __init__(self, profile: object):
        self.profile = profile

    def add(self, product: int, review: str) -> None:
        """
        Добавляет отзыв к товару
        :param product: ид товара
        :type product: int
        :param review: текст отзыва
        :type review: str
        :return: None
        :rtype: None
        """
        Review.objects.create(
            user=self.profile,
            product_id=product,
            text=review,
        )
        return None

    def get_reviews_for_product(self, product: object) -> List:
        """
        Возвращает список отзывов к товару
        :param product: товар
        :type product: object
        :return: список отзывов
        :rtype: list
        """
        reviews = Review.objects.filter(product=product)
        return reviews


def check_product_quantity(product: Product, quantity: int) -> bool:
    """Проверяет допустимое количество товара на складе"""
    return product.quantity >= quantity


def get_update_quantity_product(product: Product, user: user) -> bool:
    """
    Возвращает булево значения, для добавление товара или обновления его количетсва в корзине
    """
    update_product = False
    if not user.is_anonymous:
        cart = user.carts.get(is_active=True)
        product_in_cart = ProductInCart.objects.filter(product=product, cart=cart)
        if product_in_cart:
            update_product = True
    return update_product
