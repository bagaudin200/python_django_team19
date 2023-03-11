
from django.urls import path

from app_order.views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
]
