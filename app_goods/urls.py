from django.urls import path
from django.views.decorators.cache import cache_page
from app_goods.views import GoodsDetailView, CatalogView, ShopView, add_review

urlpatterns = [
    path('', ShopView.as_view(), name='top'),
    path('add_review', add_review, name='add_review'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('top/', ShopView.as_view(), name='top'),
    path('<str:slug>/', GoodsDetailView.as_view(), name='product'),
]
