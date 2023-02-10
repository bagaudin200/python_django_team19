from django.urls import path
from .views import GoodsDetailView, CatalogView

urlpatterns = [
    path('product/<slug:product_slug>/', GoodsDetailView.as_view(), name='product'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
]
