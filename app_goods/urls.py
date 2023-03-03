from django.urls import path
from django.views.decorators.cache import cache_page
from app_goods.views import GoodsDetailView, CatalogView


urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('<str:slug>/', cache_page(60)(GoodsDetailView.as_view()), name='product'),
]
