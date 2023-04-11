from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_settings.models import SiteSettings
from app_goods.models import Category, Product


# class TestShopView(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         category = Category.objects.create(name='test_category')
#         category.save()
#         settings = SiteSettings.objects.create(express_order_price=500, standard_order_price=200)
#         settings.save()
#         product = Product.objects.create(id=1, name='test_product', category=category, price=10,
#                                          is_limited=True)
#         product.save()
#
#     def test_main_page_exist_at_desired_location(self):
#         response = self.client.get(reverse('top'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Гарантированные платежи')
#
#     def test_main_page_used_right_template(self):
#         response = self.client.get(reverse('top'))
#         self.assertTemplateUsed(response, 'app_goods/index.jinja2')
#
#     def test_main_page_contain_right_context(self):
#         self.client.login(email='test@test.ru', password='12345')
#         response = self.client.get(reverse('top'))
#         products = response.context.get('products')
#         limited = response.context.get('is_limited')
#         self.assertEqual(1, len(products))
#         self.assertEqual(1, len(is_limited))


class TestProductView(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products', 'fixtures/images']

    def setUp(self):
        self.product = Product.objects.get(id=1)

    def test_blogs_exists_at_desired_location(self):
        response = self.client.get(reverse('product:product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)





