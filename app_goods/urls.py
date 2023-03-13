from django.urls import path
from django.views.decorators.cache import cache_page
from .views import GoodsDetailView, ShopView, CatalogView

app_name = 'goods'
urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    #path('<str:slug>/', cache_page(60)(GoodsDetailView.as_view()), name='product'),

    path('product/<str:slug>/', GoodsDetailView.as_view(), name='product'),
    path('top/', ShopView.as_view(), name='top')
]
