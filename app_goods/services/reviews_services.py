from typing import List

from django.contrib.auth import get_user_model

from app_goods.models import Review, Product

User = get_user_model()


class ReviewService:
    """Сервис для работы с отзывами"""

    def __init__(self, profile: User, product: Product):
        self.profile = profile
        self.product = product

    def add(self, review: Review) -> None:
        """
        Добавляет отзыв к товару
        """
        Review.objects.create(
            user=self.profile,
            product_id=self.product,
            text=review,
        )

    def get_reviews_for_product(self) -> List[Review]:
        """
        Возвращает список отзывов к товару
        """
        reviews = Review.objects.filter(product=self.product)
        return reviews
