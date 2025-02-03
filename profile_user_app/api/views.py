from rest_framework.response import Response
from profile_user_app.models import Profile
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
        pk = self.kwargs.get('pk')
        try:
            profiles = Profile.objects.get(user=pk)
            serializer = ProfileSerializer(profiles)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"detail": "Profil nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        try:
            profile = Profile.objects.get(user=pk)
            if not (request.user == user or request.user.is_staff):
                raise PermissionDenied("Keine Berechtigung, dieses Profil zu bearbeiten.")
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            new_username = request.data.get('username', '').strip().replace(' ', '_').lower()
            email = request.data.get('email')
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                return Response(
                    {"error": "Benutzername bereits vergeben."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                return Response(
                    {"error": "Email bereits vergeben."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            switch_username(user, profile, email)
            return Response({
                'user': user.id,
                'username': profile.username,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
                'token': request.auth.key
            }, status=status.HTTP_200_OK)
        except NotFound:
            return Response(
                {"detail": "Profil nicht gefunden"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied:
            return Response(
                {"detail": "Keine Berechtigung, dieses Profil zu bearbeiten."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except ValidationError as e:
            return Response(
                {"errors": e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )


        

def switch_username(user, profile, email):
    new_username = profile.username
    if ' ' in new_username:
        new_username = new_username.replace(' ', '_')
    username = new_username.lower()
    user.username = username
    user.email = email
    user.save()