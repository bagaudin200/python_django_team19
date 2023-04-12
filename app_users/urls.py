from django.urls import path
from .views import validate_email, validate_phone, ProfileView, MyRegistration, MyLogoutView, MyLoginView, \
    MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, MyPasswordResetCompleteView, \
    ModalLoginView, AccountView

app_name = 'users'

urlpatterns = [
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('registration/', MyRegistration.as_view(), name='registration'),
    path('validate_email', validate_email, name='validate_email'),
    path('validate_phone', validate_phone, name='validate_phone'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account/', AccountView.as_view(), name='account'),
    path('password-reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('', MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
