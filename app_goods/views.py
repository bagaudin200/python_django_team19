from django.core.cache import cache
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from app_goods.models import Product, Review
from .services import get_cheapest_product, get_most_expensive_product, get_update_quantity_product


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        obj = cache.get(f"product:{slug}")
        if not obj:
            obj = super(GoodsDetailView, self).get_object()
            cache.set(f"product:{slug}", obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['reviews'] = Review.objects.filter(product_id=product.id)
        return context



class CatalogView(FormMixin, ListView):
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['cheapest'] = get_cheapest_product(self.get_queryset())
        context['most_expensive'] = get_most_expensive_product(self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.GET:
            category_name = self.request.GET.get('category')
            return Product.objects.filter(category__name=category_name).select_related('category__parent', 'category').order_by('price')
        return Product.objects.select_related('category__parent', 'category').order_by('price')
