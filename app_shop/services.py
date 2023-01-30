from typing import List


class ViewedProductsService:
    """Сервис просмотренных товаров"""

    def __init__(self, profile):
        self.profile = profile

    def add(self, product: object) -> None:
        """
        Добавляет товар в список просмотренных
        :param product: товар
        :type product: object
        :return: None
        :rtype: None
        """
        pass

    def remove(self, product: object) -> None:
        """
        Удаляет товар из списка просмотренных
        :param product: товар
        :type product: object
        :return: None
        :rtype: None
        """
        pass

    def already_in_viewed(self, product: object) -> bool:
        """
        Есть ли товар уже в списке просмотренных
        :param product: товар
        :type product: object
        :return: True or False
        :rtype: bool
        """
        return False

    def get_items(self) -> List:
        """
        Возвращает список просмотренных товаров
        :return:
        :rtype:
        """
        return ['Товар1', 'Товар2', 'Товар3']

    def get_items_count(self) -> int:
        """
        Возвращает количество просмотренных товаров
        :return: количество просмотренных товаров
        :rtype: int
        """
        return 5


class ComparisonProductsService:
    """Сервис сравнения товаров"""

    def __init__(self, profile):
        self.profile = profile

    def add(self, product: object) -> None:
        """
        Добавляет товар в список сравнения
        :param product: товар
        :type product: object
        :return: None
        :rtype: None
        """
        pass

    def remove(self, product: object) -> None:
        """
        Удаляет товар из списка сравнения
        :param product: товар
        :type product: object
        :return: None
        :rtype: None
        """
        pass

    def get(self, maximum: int = 3) -> List:
        """
        Возвращает список товаров, добавленных к сравнению
        :param maximum: количество возвращаемых товаров (по умолчанию 3)
        :type maximum: int
        :return: список товаров, добавленных к сравнению
        :rtype: list
        """
        return ['Товар1', 'Товар2', 'Товар3', 'Товар4'][:maximum]

    def count(self) -> int:
        """
        Возвращает количество товаров, добавленных к сравнению
        :return: количество товаров, добавленных к сравнению
        :rtype: int
        """
        return 3


class DiscountService:
    """Сервис управления скидками (для администратора)"""

    def get_discounts(self, products: List) -> dict:
        """
        Возвращает все скидки на указанные товары
        :param products: список товаров
        :type products: list
        :return: словарь типа {'Товар': скидка}
        :rtype: dict
        """
        return {'Товар1': 10, 'Товар2': 15}

    def get_priority_discounts(self, products: List) -> dict:
        """
        Возвращает приоритетную скидку на указанные товары
        :param products: список товаров
        :type products: list
        :return: словарь типа {'Товар': скидка}
        :rtype: dict
        """
        return {'Товар1': 10, 'Товар2': 15}


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


def import_products(folder_path: str) -> None:
    """
    Сервис, позволяющий сделать импорт товаров из XML или JSON-файлов
    :param folder_path: путь к папке с файлами для импорта
    :type folder_path: str
    :return: None
    :rtype: None
    """
    pass
