from django.core.paginator import Paginator, InvalidPage

from app_goods.models import Category


class CatalogQueryStringBuilder:
    """
    Создает ссылки с GET-параметрами для страницы каталога
    """

    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}
    __available_params = {
        'search': 'name__icontains',
        'tag': 'tag',
        'category': 'category',
        'price': 'price__range',
        'title': 'name__icontains',
        'in_stock': 'in_stock',
        'free_delivery': 'free_delivery',
        'order_by': 'order_by',
        'order': 'order',
        'page': 'page',
    }

    def __init__(self, request, **params):
        self.request = request
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

        # query_string = ''
        # query_string_dict = self.to_dict()
        # all_params = query_string_dict | self.params
        # for key, value in all_params.items():
        #     query_string_dict[key] = value
        #     query_string += f'&{key}={value}'
        # return f'?{query_string}'

    # def to_dict(self) -> dict:
    #     query_string = self.normalize_query_string(query_string=self.request.META['QUERY_STRING'])
    #     params_list = query_string.split('&')
    #     params_dict = {}
    #     for param in params_list:
    #         name, value = param.split('=')
    #         if name in self.__available_params:
    #             params_dict[name] = value
    #     return params_dict

        # if search := self._get_search():
        #     return f'?search={search}'
        # if tag := self._get_tag():
        #     return f'?tag={tag}'
        #
        # string = ''
        # if category := self._get_category():
        #     string += f'?category={category}'
        # if prices := self._get_price_range():
        #     string += f'&price={prices[0]}-{prices[1]}'
        # if title := self._get_title():
        #     string += f'&title={title}'
        # if in_stock := self._get_in_stock():
        #     string += f'&in_stock={in_stock}'
        # if free_delivery := self._get_free_delivery():
        #     string += f'&free_delivery={free_delivery}'
        # if order_by := self._get_order_by():
        #     string += f'&order_by={order_by}'
        # if order := self._get_order():
        #     string += f'&order={order}'
        # if page := self._get_page():
        #     string += f'&page={page}'
        #
        # return string

    def _get_category(self):
        category = self.request.GET.get('category')
        if category not in Category.objects.values_list('slug', flat=True):
            return None
        return Category.objects.get(slug=category)

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

    def _get_price_range(self):
        prices = self.request.GET.get('price')
        return tuple(prices.split(';')) if prices else (None, None)

    def _get_title(self):
        return self.request.GET.get('title')

    def _get_in_stock(self):
        in_stock = self.request.GET.get('in_stock')
        try:
            result = bool(int(in_stock))
            return result
        except (TypeError, ValueError):
            return False

    def _get_free_delivery(self):
        free_delivery = self.request.GET.get('free_delivery')
        try:
            result = bool(int(free_delivery))
            return result
        except (TypeError, ValueError):
            return False

    def _get_tag(self):
        tag = self.request.GET.get('tag')
        return tag

    def _get_search(self):
        search = self.request.GET.get('search')
        return search

    def _get_page(self):
        page = self.request.GET.get('page')
        return page

    def normalize_query_string(self, query_string):
        if query_string[0] == '&':
            return query_string[1:]
        return query_string

    def filter_kwargs(self) -> dict:
        params_list = self.request.META['QUERY_STRING'].split('&')
        params_dict = {}
        for param in params_list:
            name, value = param.split('=')
            if name in self.__available_params:
                params_dict[self.__available_params[name]] = value
        return params_dict


class CatalogPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except InvalidPage:
            if int(number) > 1:
                return self.num_pages
            return 1
