from typing import List, Tuple, Any

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpRequest

from app_goods.models import Review, Product

User = get_user_model()


class ReviewsService:
    """Сервис для работы с отзывами"""

    def __init__(self, request: HttpRequest, profile: User, product: Product):
        self.request = request
        self.product = product
        self.profile = profile

    def add(self, review: str) -> None:
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
        reviews = Review.objects.filter(product=self.product).order_by('-created_at')
        return reviews

    def paginate(self, reviews: List[Review]) -> Tuple[Paginator, Any]:
        """Передает пагитатор для работы пагинации отзывов о товарах"""
        paginator = Paginator(reviews, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return paginator, page_obj
