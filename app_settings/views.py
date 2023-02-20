import json

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect


def clear_all_cache_view(request):
    """Очистка всего кеша"""
    cache.clear()
    messages.success(request, 'All cache is cleared')
    return redirect(request.META.get('HTTP_REFERER'))

def top_catalog_product(request):
    """Каталог топ товаров на главной странице"""
    return render(request, 'app_shop/index.jinja2')