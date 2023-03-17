from django.urls import path
from . import views


urlpatterns = [
    path('step_1/', views.OrderStepOneView.as_view(), name='order_step_1'),
    path('step_2/', views.OrderStepTwoView.as_view(), name='order_step_2'),
    path('step_3/', views.OrderStepThreeView.as_view(), name='order_step_3'),
]
