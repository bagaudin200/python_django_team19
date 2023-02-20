from django.core.cache import cache
from django.db.models import Sum
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from app_goods.models import Product, Review
from app_settings.models import SiteSettings
from .services import get_cheapest_product, get_most_expensive_product


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



class ShopView(TemplateView):
    template_name = 'index.html'

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