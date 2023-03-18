from django.urls import path
from app_order.views import OrderListView, OrderDetailView, OrderView

app_name = 'order'

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('history/', OrderListView.as_view(), name='history'),
    path('history/<int:pk>/', OrderDetailView.as_view(), name='detail_order'),
]

