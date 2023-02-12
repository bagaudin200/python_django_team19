from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from app_goods.models import Product, Category
from .services import get_cheapest_product, get_most_expensive_product


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class CatalogView(FormMixin, ListView):
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginate_by = 8
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['orders_by'] = self.__order_by
        # context['cheapest'] = get_cheapest_product(self.get_queryset())
        # context['most_expensive'] = get_most_expensive_product(self.get_queryset())
        return context

    def get_queryset(self):
        category = self._get_category()
        order = self._get_order()
        order_by = self._get_order_by()

        qs = Product.objects.select_related('category', 'category__parent')
        if category:
            filter_kwargs = dict(category__parent=category) if category.get_children() else dict(category=category)
            qs = qs.filter(**filter_kwargs)
        qs = qs.order_by(f"{order}{order_by}")
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
        return order_by
