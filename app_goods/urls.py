from django.urls import path
from .views import GoodsDetailView

urlpatterns = [
    path('product/<slug:product_slug>/', GoodsDetailView.as_view(), name='product'),
]
