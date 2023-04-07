from django.test import TestCase

from app_goods.models import Product


class ProductTestCase(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products']

    def setUp(self):
        pass



