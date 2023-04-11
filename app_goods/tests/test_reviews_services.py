from django.contrib.auth import get_user_model
from django.test import TestCase

from app_goods.models import Product, Review
from app_goods.services.reviews_services import ReviewsService

User = get_user_model()


class ReviewsTestCase(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products', 'fixtures/images']

    def setUp(self):
        self.user = User.objects.create(full_name='TestUserName')
        self.product = Product.objects.get(id=1)
        self.reviews_service = ReviewsService(self.client, self.user, self.product.id)

    def test_add(self):
        try:
            reviews = Review.objects.get(product=self.product)
        except Review.DoesNotExist:
            reviews = False
        self.assertFalse(reviews)
        self.reviews_service.add('TestReview')
        reviews = Review.objects.get(product=self.product)
        self.assertTrue(reviews)

    def test_reviews_for_product(self):
        num = 4
        for _ in range(num):
            self.reviews_service.add('TestReview')
        reviews = self.reviews_service.get_reviews_for_product()
        self.assertEqual(reviews.count(), num)
