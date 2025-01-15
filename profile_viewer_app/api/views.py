from rest_framework.response import Response
from profile_viewer_app.models import ProfileViewer
from .serializers import ProfileViewerSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
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
    
    def post(self, request):
        serializer = ProfileViewerSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.viewer_id = instance.pk
            instance.save()
            response_serializer = ProfileViewerSerializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = ProfileViewer.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user=user_id)
        return queryset

    
class ProfileSinglViewSets(generics.ListCreateAPIView):  
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileViewerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            raise PermissionDenied("POST-Anfragen sind für diesen Endpunkt nicht erlaubt.")
        if self.request.method in ['PATCH']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
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
        