from django.urls import path
from .views import RegistrationView, ActivateAccountView, PasswordResetRequestView, PasswordResetConfirmView, OldPasswordResetView

urlpatterns = [
  path('registration/', RegistrationView.as_view(), name='registration_app'),
  path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate_account'),
  path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
  path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('old_password_reset/', OldPasswordResetView.as_view(), name='password_reset_confirm'),
]





























