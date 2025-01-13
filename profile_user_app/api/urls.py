from django.urls import path
from .views import ProfileViewSets

urlpatterns = [
    path('<int:pk>/', ProfileViewSets.as_view(), name='profile-detail'),
]
