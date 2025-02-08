from rest_framework import permissions
from profile_viewer_app.models import ProfileViewer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user or request.user.is_staff:
            return True     
        return False
    
