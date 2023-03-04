from django.urls import path
from .views import GoodsDetailView, ShopView, CatalogView, AddReview

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('<str:slug>/', GoodsDetailView.as_view(), name='product'),
    path('add_review/', AddReview.as_view(), name='add_review'),
    path('top/', ShopView.as_view(), name='top'),
]
