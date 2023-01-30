import random
import re
from typing import Any

re_card_number_pattern = r"^\d{7}[2,4,6,8]$"  # 8-значное четное число, не заканчивающееся на 0


def card_number_is_valid(card_number: Any) -> bool:
    """
    Проверяет, является ли номер карты 8-значным четным числом, не заканчивающимся на 0
    :param card_number: номер карты
    :type card_number: int
    :return: True or False
    :rtype: bool
    """
    return True if re.fullmatch(re_card_number_pattern, card_number) else False


def generate_card_number() -> int:
    """
    Генерирует номер карты, являющийся 8-значным четным числом, не заканчивающимся на 0
    :return: номер карты
    :rtype: int
    """
    random_number = random.randrange(10000002, 99999999, 2)
    if random_number % 10 == 0:
        random_number -= 2
    return random_number
