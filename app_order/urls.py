from django.urls import path
from . import views
from .views import OrderListView, OrderDetailView

app_name = 'order'

urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('history/', OrderListView.as_view(), name='history'),
    path('history/<int:pk>/', OrderDetailView.as_view(), name='detail_order'),
]
