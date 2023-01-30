from django.test import TestCase
from .utils import card_number_is_valid, generate_card_number


class TestUtils(TestCase):
    EXPECTED = {
        '1000002': False,
        '10000000': False,
        '10000001': False,
        '10000002': True,
        '10000004': True,
        '10000006': True,
        '10000008': True,
        '10000010': False,
        '99999990': False,
        '99999991': False,
        '99999992': True,
        '99999993': False,
        '99999994': True,
        '99999995': False,
        '99999996': True,
        '99999997': False,
        '99999998': True,
        '99999999': False,
        '100000000': False,
        '100000001': False,
        '100000002': False,
    }

    def test_card_number_is_valid(self):
        result = {}
        for key in self.EXPECTED:
            result[key] = card_number_is_valid(card_number=key)
        self.assertEqual(self.EXPECTED, result)

    def test_generate_card_number(self):
        for _ in range(1000):
            self.assertTrue(card_number_is_valid(str(generate_card_number())))
