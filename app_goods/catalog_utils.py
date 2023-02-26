from abc import abstractmethod
from typing import Any
from decimal import Decimal
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from app_goods.models import Category, Product


class Builder:

    __available_params = (
        'search', 'tag', 'category', 'price', 'title', 'in_stock', 'free_delivery', 'order_by', 'order', 'page',
    )

    def __init__(self, request):
        self.request = request

    @abstractmethod
    def build(self) -> Any:
        pass

    def query_string_to_dict(self) -> dict:
        """
        Преобразует строку запроса в словарь
        :return: dict
        """
        query_string: str = self.request.META['QUERY_STRING']

        result = {}
        params = [param for param in query_string.split('&') if param]
        for item in params:
            name, value = item.split('=')
            if name in self.__available_params:
                result[name] = value
        return result


class CatalogQueryStringBuilder(Builder):
    """
    Создает строку запроса для страницы каталога
    """

    def __init__(self, request, **params):
        super().__init__(request)
        self.params = params

    def build(self) -> str:
        """
        Создает строку запроса из существующей строки запроса и добавляет к ней передаваемые через **params параметры
        :return: str
        """
        query_string = '?'

        all_params = self.query_string_to_dict() | self.params
        for param_name, param_value in all_params.items():
            query_string += f"&{param_name}={param_value}"
        return query_string


class CatalogQuerySetBuilder(Builder):
    """
    Создает QuerySet для каталога
    """
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}
    __filter_params = ('search', 'tag', 'category', 'price', 'title', 'in_stock', 'free_delivery',)

    def build(self) -> QuerySet:
        """
        Создает QuerySet для каталога
        :return: QuerySet
        """

        # Начальный qs по умолчанию отсортирован по возрастанию цены
        qs = Product.objects.select_related('category', 'category__parent').defer('description').order_by('price')

        # Собираем все фильтры в словарь filter_params
        filter_params = {}
        for param_name in self.query_string_to_dict().keys():
            if param_name in self.__filter_params:
                filter_params.update(self.functions[param_name]())

        # Добавляем к qs сортировку
        order_by = self._get_order_by()
        order = self._get_order()

        # Формируем итоговый qs
        qs = qs.filter(**filter_params).order_by(f"{order}{order_by}")
        return qs

    @property
    def functions(self):
        return {
            'category': self._get_category_filter,
            'price': self._get_price_range_filter,
            'title': self._get_title_filter,
            'in_stock': self._get_in_stock_filter,
            'free_delivery': self._get_free_delivery_filter,
            'tag': self._get_tag_filter,
            'search': self._get_search_filter,
        }

    def _get_category_filter(self) -> dict:
        category = self.request.GET.get('category')
        try:
            cat = Category.objects.get(slug=category)
            if cat.get_children():
                return dict(category__parent=cat)
            return dict(category=cat)
        except ObjectDoesNotExist:
            return dict()

    def _get_order(self):
        order = self.request.GET.get('order')
        if order == 'desc':
            return '-'
        return ''

    def _get_order_by(self):
        order_by = self.request.GET.get('order_by')
        if not (order_by in self.__order_by):
            return 'price'
        if order_by == 'novelty':
            order_by = 'created_at'
        return order_by

    def _get_price_range_filter(self) -> dict:
        prices = self.request.GET.get('price')
        try:
            price_from, price_to = prices.split(';')
            return dict(price__range=[Decimal(price_from), Decimal(price_to)])
        except Exception as e:
            print(e)
            return dict()

    def _get_title_filter(self) -> dict:
        title = self.request.GET.get('title')
        if title:
            return dict(name__icontains=title)
        return dict()

    def _get_in_stock_filter(self) -> dict:
        in_stock = self.request.GET.get('in_stock')
        try:
            result = int(in_stock)
            return dict(quantity__gt=0) if result else dict()
        except (TypeError, ValueError):
            return dict()

    def _get_free_delivery_filter(self) -> dict:
        free_delivery = self.request.GET.get('free_delivery')
        try:
            result = bool(int(free_delivery))
            return dict(free_delivery=result)
        except (TypeError, ValueError):
            return dict()

    def _get_tag_filter(self) -> dict:
        tag = self.request.GET.get('tag')
        return dict(tag__slug=tag)

    def _get_search_filter(self) -> dict:
        search = self.request.GET.get('search')
        return dict(name__icontains=search)


class CatalogPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except InvalidPage:
            if int(number) > 1:
                return self.num_pages
            return 1
