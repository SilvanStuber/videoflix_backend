from rest_framework import serializers
from profile_user_app.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [    
            'user',       
            'username', 
            'first_name',
            'last_name',
            'email',
            'created_at',
        ]