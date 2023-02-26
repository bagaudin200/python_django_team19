from django.core.paginator import Page
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Sum
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from app_goods.models import Product, Category
from .forms import FilterForm
from .services import get_cheapest_product_price, get_most_expensive_product_price
from .catalog_utils import CatalogPaginator, CatalogQueryStringBuilder, CatalogQuerySetBuilder
from app_goods.models import Product, Review
from app_settings.models import SiteSettings


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        print(self.kwargs)
        slug = self.kwargs['slug']
        obj = cache.get(f"product:{slug}")
        if not obj:
            obj = super(GoodsDetailView, self).get_object()
            cache.set(f"product:{slug}", obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product_id=self.object.id)
        return context


class CatalogView(FormMixin, ListView):
    form_class = FilterForm
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginator_class = CatalogPaginator
    paginate_by = 8
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}
    queryset = Product.objects.select_related('category', 'category__parent').defer('description', 'quantity').order_by(
        'price')

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['orders_by'] = self.__order_by
        context['cheapest'] = get_cheapest_product_price(self.queryset)
        context['most_expensive'] = get_most_expensive_product_price(self.queryset)
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        context['popular_tags'] = Product.tags.most_common()[:20]
        context['query_string_builder'] = CatalogQueryStringBuilder
        return context

    def get_queryset(self):
        builder = CatalogQuerySetBuilder(request=self.request)
        return builder.build()


class ShopView(TemplateView):
    template_name = 'app_goods/index.jinja2'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        quantity = SiteSettings.load()
        context['products'] = Product.objects. \
                                  prefetch_related('order_items'). \
                                  filter(available=True). \
                                  only('category', 'name', 'price'). \
                                  annotate(total=Sum('order_items__quantity')). \
                                  order_by('-total')[:quantity.quantity_popular]
        context['is_limited'] = Product.objects. \
            select_related('category'). \
            filter(available=True). \
            filter(limited=True). \
            only('category', 'name', 'price')
        return context
