from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('with-card/', views.PaymentWithCardView.as_view(), name='payment_with_card'),
    path('someone-account/', views.PaymentFromSomeonesAccount.as_view(), name='payment_someone'),
    path('progress/', views.ProgressPaymentView.as_view(), name='progress_payment'),
]
