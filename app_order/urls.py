from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderView.as_view(), name='order'),
    path('user/', views.user_order, name='test'),
]
