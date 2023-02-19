from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from app_goods.models import Product, Category
from .forms import FilterForm
from .services import get_cheapest_product_price, get_most_expensive_product_price


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class CatalogView(FormMixin, ListView):
    form_class = FilterForm
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginate_by = 8
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}
    queryset = Product.objects.select_related('category', 'category__parent').defer('description', 'quantity')

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['orders_by'] = self.__order_by
        context['cheapest'] = get_cheapest_product_price(self.queryset)
        context['most_expensive'] = get_most_expensive_product_price(self.queryset)
        return context

    def get_queryset(self):
        category = self._get_category()
        order = self._get_order()
        order_by = self._get_order_by()
        price_from, price_to = self._get_price_range()
        name = self.request.GET.get('title')
        in_stock = self._get_in_stock()
        free_delivery = self._get_free_delivery()

        qs = self.queryset
        if category:
            filter_kwargs = dict(category__parent=category) if category.get_children() else dict(category=category)
            qs = qs.filter(**filter_kwargs)
        if price_from and price_to:
            qs = qs.filter(price__range=[price_from, price_to])
        if name:
            qs = qs.filter(name__icontains=name)
        if in_stock:
            qs = qs.filter(quantity__gt=0)
        if free_delivery:
            qs = qs.filter(free_delivery=free_delivery)
        qs = qs.order_by(f"{order}{order_by}")
        self.queryset = qs
        return qs

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

    def _get_in_stock(self):
        in_stock = self.request.GET.get('in_stock')
        try:
            result = bool(int(in_stock))
            return result
        except:
            return False

    def _get_free_delivery(self):
        free_delivery = self.request.GET.get('free_delivery')
        try:
            result = bool(int(free_delivery))
            return result
        except:
            return False
