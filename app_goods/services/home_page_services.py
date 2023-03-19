from django.db.models import QuerySet

from app_goods.models import Product, Category
from app_settings.models import SiteSettings


class HomePageServices:
    """Сервис для работы с главной страницей"""

    def __init__(self):
        self.site_settings = SiteSettings.load()
        self.products_queryset = Product.objects.select_related('category', 'category__parent').defer('description')

    def get_top_categories(self) -> QuerySet:
        """
        Возвращает топ категорий на главной странице
        :return: топ категорий на главной странице
        """
        return Category.objects.filter(level=1).prefetch_related(
            'product_set').order_by('-product__sales_count').distinct()[:self.site_settings.banners_count]

    def get_most_popular_products(self) -> QuerySet:
        """
        Возвращает самые популярные товары по продажам
        :return: самые популярные товары по продажам
        """
        return self.products_queryset.order_by('-sales_count')[:self.site_settings.top_items_count]

    def get_limited_products(self) -> QuerySet:
        """
        Возвращает случайные limited-товары
        :return: случайные limited-товары
        """
        return self.products_queryset.filter(is_limited=True).order_by('?')[:self.site_settings.limited_edition_count]
