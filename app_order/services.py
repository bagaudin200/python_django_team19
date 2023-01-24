from typing import List


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, profile):
        self.profile = profile

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
