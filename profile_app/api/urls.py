from django.urls import path
from .views import ProfileViewSets, ProfileCustomerViewSets, ProfileBusinessViewSets

urlpatterns = [
    path('<int:pk>/', ProfileViewSets.as_view(), name='profile-detail'),
]
