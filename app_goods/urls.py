from django.urls import path
from .views import GoodsDetailView, ShopView

urlpatterns = [
    path('product/<slug:product_slug>/', GoodsDetailView.as_view(), name='product'),
    path('top/', ShopView.as_view(), name='top')
]
