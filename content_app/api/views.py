from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from content_app.models import Video
from .serializers import VideoListSerializer, VideoDetailSerializer


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    lookup_field = 'id'  


class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.order_by('-created_at')[:10]  
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)
