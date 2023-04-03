from django.urls import path
from app_cart.views import CartDetail, get_cart_data, cart_add, cart_remove, cart_add_from_product_card

app_name = 'cart'

urlpatterns = [
    path('cart_detail/', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('add_from_product_card/<int:pk>/', cart_add_from_product_card, name='cart_add_from_product_card'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('get_cart_data/', get_cart_data, name='get_cart_data'),
]
