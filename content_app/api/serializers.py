from rest_framework import serializers
from content_app.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title']  # Falls du ein Thumbnail hast, ergänze 'thumbnail'

class VideoDetailSerializer(serializers.ModelSerializer):
    video_720p = serializers.SerializerMethodField()
    video_480p = serializers.SerializerMethodField()


    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'video_file', 'video_720p', 'video_480p',]

    def get_video_720p(self, obj):
        if obj.video_file:
            return obj.video_file.url.replace('.mp4', '_720p.mp4')
        return None

    def get_video_480p(self, obj):
        if obj.video_file:
            return obj.video_file.url.replace('.mp4', '_480p.mp4')
        return None




