from django.urls import path
from .views import GoodsDetailView, CatalogView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('<slug:slug>/', cache_page(60)(GoodsDetailView.as_view()), name='product'),

]
