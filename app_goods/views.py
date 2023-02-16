from django.shortcuts import render
from django.views.generic import DetailView
from app_goods.models import Items


class GoodsDetailView(DetailView):
    model = Items
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'


class ShopView(TemplateView):
    template_name = 'app_goods/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        quantity = SiteSettings.load()
        context['products'] = Product.objects. \
                                  prefetch_related('order_items'). \
                                  filter(available=True). \
                                  only('category', 'name', 'price'). \
                                  annotate(total=Sum('order_items__quantity')). \
                                  order_by('-total')[:quantity.quantity_popular]
        context['limited'] = Product.objects. \
            select_related('category'). \
            filter(available=True). \
            filter(limited=True). \
            only('category', 'name', 'price')
        return context





