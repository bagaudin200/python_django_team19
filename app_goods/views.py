from django.shortcuts import render
from django.views.generic import DetailView
from app_goods.models import Items


class GoodsDetailView(DetailView):
    model = Items
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'





