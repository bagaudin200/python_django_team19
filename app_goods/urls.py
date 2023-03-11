from django.urls import path
from django.views.decorators.cache import cache_page
from app_goods.views import GoodsDetailView, CatalogView, ShopView


urlpatterns = [
    path('', ShopView.as_view(), name='top'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('<str:slug>/', cache_page(60)(GoodsDetailView.as_view()), name='product'),

    path('product/<str:slug>/', GoodsDetailView.as_view(), name='product'),
    path('top/', ShopView.as_view(), name='top')
]
