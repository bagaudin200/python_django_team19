from django.urls import path
from .views import cart_add
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('cart_add/', cart_add, name='cart_add'),
]
