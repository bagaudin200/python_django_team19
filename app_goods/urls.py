from django.urls import path
from django.views.decorators.cache import cache_page
from app_goods.views import GoodsDetailView, CatalogView, HomePageView, add_review

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_review/', add_review, name='add_review'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('product/<str:slug>/', GoodsDetailView.as_view(), name='product'),
]
