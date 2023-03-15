from typing import List

from django.contrib.auth import get_user_model

from app_cart.models import Cart
from app_goods.models import Product, Review
from app_settings.models import SiteSettings
from app_users.forms import User

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


def get_top_products() -> Product:
    """
    Возвращает самые популярные товары
    :param products:
    :return: самые популярные товары
    """
    quantity = SiteSettings.load()
    return Product.objects.only('category', 'name', 'price')\
                  .order_by('quantity')[:quantity.top_items_count]


def get_limited_product() -> Product:
    """
    Возвращает топ ограниченных товаров
    :param is_limited:
    :return: топ ограниченных товаров
    """
    return Product.objects.select_related('category')\
                          .filter(is_limited=True)\
                          .only('category', 'name', 'price')


def check_product_quantity(product: Product, quantity: int) -> bool:
    """Проверяет допустимое количество товара на складе"""
    if product.quantity >= quantity:
        return True
    return False


def get_update_quantity_product(product: Product, user: User) -> bool:
    """
    Возвращает булево значения, для добавление товара или обновления его количетсва в корзине
    """
    update_product = False
    if not user.is_anonymous:
        cart = Cart.objects.filter(user=user, good=product)
        if cart:
            update_product = True
    else:
        pass
    return update_product
