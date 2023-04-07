from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpRequest

from app_cart.models import ProductInCart, Cart
from app_goods.models import Product, Image
from app_settings.models import SiteSettings

User = get_user_model()


class ProductService:
    """Сервис для работы с товаром"""

    def __init__(self, request: HttpRequest, product: Product, slug):
        self.product = product
        self.request = request
        self.slug = slug
        self.profile = request.user

    def check_product_quantity(self, quantity: int) -> bool:
        """Проверяет допустимое количество товара на складе"""
        return self.product.quantity >= quantity

    def get_update_quantity_product(self) -> bool:
        """
        Возвращает булево значения, для добавление товара или обновления его количетсва в корзине
        """
        update_product = False
        if not self.profile.is_anonymous:
            product_in_cart = ProductInCart.objects.filter(
                product=self.product,
                cart=Cart.objects.filter(user=self.profile, is_active=True).first())
            if product_in_cart:
                update_product = True
        else:
            product_id = str(self.product.id)
            if product_id in self.request.session[settings.CART_SESSION_ID]:
                update_product = True

        return update_product

    def get_product_quantity(self):
        return self.product.quantity

    def get_images(self) -> Image:
        """
        Возвращает изображения товара из кеша или из базы данных
        """
        images = cache.get(f"images:{self.slug}")
        if not images:
            images = Image.objects.filter(product=self.product)
            cache.set(f"images:{self.slug}", images, SiteSettings.load().product_cache_time)
        return images
