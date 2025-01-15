from django.urls import path
from .views import ProfileViewSets, ProfileSinglViewSets

urlpatterns = [
    path('', ProfileViewSets.as_view(), name='profile_viewer_app'),
    path('<int:pk>/', ProfileSinglViewSets.as_view(), name='profile_viewer_appl'),
]
