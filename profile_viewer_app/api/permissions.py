from rest_framework import permissions
from profile_viewer_app.models import ProfileViewer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user or request.user.is_staff:
            return True     
        return False  

class IsOwnerFromViewerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        viewer_id = view.kwargs.get("pk")
        if viewer_id is None:
            return False
        try:
            viewer = ProfileViewer.objects.get(pk=viewer_id)
        except ProfileViewer.DoesNotExist:
            return False
        return request.user.pk == viewer.user or request.user.is_staff




