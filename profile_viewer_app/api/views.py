from rest_framework.response import Response
from profile_viewer_app.models import ProfileViewer
from .serializers import ProfileViewerSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsOwnerFromViewerOrAdmin
from django.contrib.auth.models import User

class ProfileViewSets(generics.ListCreateAPIView):  
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileViewerSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        try:
            user = self.request.query_params.get('user') 
            if user:
                return ProfileViewer.objects.filter(user=user)
        except user.DoesNotExist:
            return Response({"detail": "Profile nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
   
    def post(self, request):
        serializer = ProfileViewerSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.viewer_id = instance.pk
            instance.save()
            user_id = request.data.get('user')
            queryset = ProfileViewer.objects.filter(user=user_id)
            serialized_data = ProfileViewerSerializer(queryset, many=True).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class ProfileSinglViewSets(generics.ListCreateAPIView):  
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileViewerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            raise PermissionDenied("POST-Anfragen sind für diesen Endpunkt nicht erlaubt.")
        if self.request.method in ['PATCH']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        if self.request.method in ['GET', 'DELETE']:
            permission_classes = [IsAuthenticated, IsOwnerFromViewerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            viewer = ProfileViewer.objects.get(pk=pk)
            serialized_data = ProfileViewerSerializer(viewer).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except ProfileViewer.DoesNotExist:
            return Response({"detail": "Profil nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, *args, **kwargs):
        pk = request.data.get('user')
        user = User.objects.get(pk=pk)
        viewer_id = self.kwargs.get('pk')
        try:
            viewer = ProfileViewer.objects.get(pk=viewer_id)
            if not (request.user == user or request.user.is_staff):
                raise PermissionDenied("Keine Berechtigung, dieses Profil zu bearbeiten.")
            serializer = ProfileViewerSerializer(viewer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"detail": "Profil nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": "Keine Berechtigung, dieses Profil zu bearbeiten."}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        viewer_id = self.kwargs.get('pk')
        viewer = ProfileViewer.objects.get(pk=viewer_id)
        user = User.objects.get(pk=viewer.user)
        try:
            viewer = ProfileViewer.objects.get(pk=viewer_id)
            if not (request.user == user or request.user.is_staff):
                raise PermissionDenied("Keine Berechtigung, dieses Profil zu löschen.")
            viewer.delete()
            return Response({"detail": "Profil erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)
        except ProfileViewer.DoesNotExist:
            return Response({"detail": "Profil nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)
        