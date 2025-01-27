from rest_framework import serializers
from profile_viewer_app.models import ProfileViewer

class ProfileViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileViewer
        fields = [    
            'user',       
            'viewer_id', 
            'viewername',
            'picture_file',
        ]   

