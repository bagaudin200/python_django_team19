from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('step_1/', views.OrderStepOneView.as_view(), name='order_step_1'),
    path('step_2/', views.OrderStepTwoView.as_view(), name='order_step_2'),
    path('step_3/', views.OrderStepThreeView.as_view(), name='order_step_3'),
    path('step_4/', views.OrderStepFourView.as_view(), name='order_step_4'),
    path('history/', views.OrderListView.as_view(), name='history'),
    path('history/<int:pk>/', views.OrderDetailView.as_view(), name='detail_order'),
]

