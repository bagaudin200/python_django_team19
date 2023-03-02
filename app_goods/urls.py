from django.urls import path
from .views import GoodsDetailView, CatalogView, AddReview

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('<slug:slug>/',GoodsDetailView.as_view(), name='product'),
    path('add_review/', AddReview.as_view(), name='add_review')

]
