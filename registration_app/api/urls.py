from django.urls import path
from .views import RegistrationView, ActivateAccountView

urlpatterns = [
  path('registration/', RegistrationView.as_view(), name='registration_app'),
  path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate_account'),
]





























