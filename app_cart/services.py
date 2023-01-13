class Cart:

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
