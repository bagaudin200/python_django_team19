from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from importlib import import_module
from django.conf import settings

from app_cart.models import Cart, ProductInCart
from app_goods.models import Product, Image
from app_goods.services.product_services import ProductService

User = get_user_model()


class ProductTestCase(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products', 'fixtures/images']

    def setUp(self):
        self.user = User.objects.create(full_name='TestUserName')
        self.anonymous_user = AnonymousUser()
        self.product = Product.objects.get(id=1)
        self.product_service = ProductService(self.client, self.user, self.product, 'TestSlug')

    def test_check_product_quantity(self):
        quantity = self.product.quantity
        result = self.product_service.check_product_quantity(quantity)
        self.assertTrue(result)
        result = self.product_service.check_product_quantity(quantity + 1)
        self.assertFalse(result)
        if quantity >= 2:
            result = self.product_service.check_product_quantity(quantity - 1)
            self.assertTrue(result)

    def test_check_update_quantity_product_true(self):
        cart = Cart.objects.create(
            user=self.user
        )
        product = ProductInCart.objects.create(
            product=Product.objects.get(id=1),
            cart=cart,
            quantity=1,
        )
        result = self.product_service.get_update_quantity_product()
        self.assertTrue(result)
        product.delete()

        cart = Cart.objects.create(
            user=self.user
        )
        ProductInCart.objects.create(
            product=Product.objects.get(id=2),
            cart=cart,
            quantity=1,
        )
        result = self.product_service.get_update_quantity_product()
        self.assertFalse(result)

    def test_get_product_quantity(self):
        quantity = self.product.quantity
        result = self.product_service.get_product_quantity()
        self.assertEqual(quantity, result)

    def test_get_images(self):
        images = Image.objects.filter(product=self.product)
        result = self.product_service.get_images()
        self.assertEqual(type(images), type(result))
        self.assertEqual(images.count(), result.count())





















