from django.urls import path
from .views import GoodsDetailView, ShopView, CatalogView, add_review

app_name = 'goods'
urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('add_review/', add_review, name='add_review'),
    path('top/', ShopView.as_view(), name='top'),
    path('<str:slug>/', GoodsDetailView.as_view(), name='product'),
]
