from django.test import TestCase
from django.urls import reverse

from app_goods.models import Product


class TestProductView(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products', 'fixtures/images']

    def setUp(self):
        self.product = Product.objects.get(id=1)

    def test_blogs_exists_at_desired_location(self):
        response = self.client.get(reverse('product:product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)
