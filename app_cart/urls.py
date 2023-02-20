from django.urls import path
from .views import cart_add

urlpatterns = [
    path('cart_add/', cart_add, name='cart_add'),
]
