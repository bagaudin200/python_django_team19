from typing import List


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
