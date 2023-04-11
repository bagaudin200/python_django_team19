from django.urls import path
from app_goods.views import GoodsDetailView, CatalogView, HomePageView, add_review

app_name = 'product'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_review/', add_review, name='add_review'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('product/<str:slug>/', GoodsDetailView.as_view(), name='product'),
]
