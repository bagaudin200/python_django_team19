from django.urls import path
from app_shop.views import top_catalog_product

urlpatterns = [
    path('index/', top_catalog_product, name='index')
]