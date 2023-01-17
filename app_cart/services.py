from typing import List


class Cart:

    def __init__(self, profile: object):
        self.profile = profile

    def add(self, product: object, quantity: int = 1, update_quantity: bool = False) -> None:
        """
        Добавление товара в корзину или обновление его количества
        :param product: товар
        :type product: object
        :param quantity: количество добавляемого товара
        :type quantity: int
        :param update_quantity: флаг, указывающий на необходимость обновления количества товара
        :type update_quantity: bool
        :return: None
        :rtype: None
        """
        pass

    def remove(self, product: object) -> None:
        """
        Удаление товара из корзины
        :param product: товар
        :type product: object
        :return: None
        :rtype: None
        """
        pass

    def clear(self) -> None:
        """
        Очистка корзины
        :return: None
        :rtype: None
        """
        pass

    def get_items(self) -> List:
        """
        Получения списка товаров в корзине
        :return: список товаров в корзине
        :rtype: list
        """
        return ['Товар1', 'Товар2', 'Товар3']

    def get_items_count(self) -> int:
        """
        Получение количества товаров в корзине
        :return: количество товаров в корзине
        :rtype: int
        """
        return 3
