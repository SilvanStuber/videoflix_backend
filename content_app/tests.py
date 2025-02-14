from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from content_app.models import Video
from content_app.api.serializers import VideoListSerializer, VideoDetailSerializer
from django.urls import reverse
from django.test import TestCase
from content_app.models import Video
from django.db.models.signals import post_save
from content_app.signals import video_post_save

User = get_user_model()

class VideoTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_save.disconnect(video_post_save, sender=Video)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        post_save.connect(video_post_save, sender=Video)

class VideoModelTest(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Beschreibung",
            titel_picture_file="img/test.png",
            video_file="videos/test.mp4",
        )

    def test_video_creation(self):
        self.assertEqual(str(self.video), "Test Video")
        self.assertEqual(self.video.description, "Test Beschreibung")
        self.assertTrue(self.video.created_at)


class VideoSerializerTest(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Beschreibung",
            titel_picture_file="img/test.png",
            video_file="videos/test.mp4",
        )

    def test_video_list_serializer(self):
        serializer = VideoListSerializer(instance=self.video)
        expected_data = {
            'id': self.video.id,
            'title': "Test Video",
            'titel_picture_file': self.video.titel_picture_file.url,
            'description': "Test Beschreibung",
            }
        self.assertEqual(serializer.data, expected_data)

    def test_video_detail_serializer(self):
        serializer = VideoDetailSerializer(instance=self.video)
        expected_data = {
            'id': self.video.id,
            'title': "Test Video",
            'description': "Test Beschreibung",
            'video_file': self.video.video_file.url,
            'video_720p': self.video.video_file.url.replace('.mp4', '_720p.mp4'),
            'video_480p': self.video.video_file.url.replace('.mp4', '_480p.mp4'),
        }
        self.assertEqual(serializer.data, expected_data)


class VideoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.video1 = Video.objects.create(
            title="Test Video 1",
            description="Test Beschreibung 1",
            video_file="videos/test1.mp4",
        )

        self.video2 = Video.objects.create(
            title="Test Video 2",
            description="Test Beschreibung 2",
            video_file="videos/test2.mp4",
        )

    def test_get_video_list(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Test Video 2")
        self.assertEqual(response.data[1]['title'], "Test Video 1")

    def test_get_video_detail(self):
        url = reverse('video-detail', args=[self.video1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Video 1")
        self.assertEqual(response.data['description'], "Test Beschreibung 1")

    def test_video_list_requires_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('video-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_detail_requires_authentication(self):
        self.client.force_authenticate(user=None)
        url = reverse('video-detail', args=[self.video1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

