from rest_framework.response import Response
from profile_app.models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .permissions import IsOwnerOrAdmin


class ProfileViewSets(generics.ListCreateAPIView):  
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            profiles = Profile.objects.get(user=pk)
            serializer = ProfileSerializer(profiles)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
                "detail": "Profil nicht gefunden"
            }, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        try:
            profile = Profile.objects.get(user=pk)
            if not (request.user == user or request.user.is_staff):
                raise PermissionDenied("Keine Berechtigung, dieses Profil zu bearbeiten.")
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            switch_username(user, profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
                "detail": "Profil nicht gefunden"
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({
                "detail": "Keine Berechtigung, dieses Profil zu bearbeiten."
            }, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        

def switch_username(user, profile):
    new_username = profile.username
    if ' ' in new_username:
        new_username = new_username.replace(' ', '_')
    username = new_username.lower()
    user.username = username
    user.save()