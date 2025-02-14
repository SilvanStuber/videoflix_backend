from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from profile_user_app.models import Profile

class ProfileAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="testuser1", email="test1@example.com", password="password123")
        self.profile1 = Profile.objects.create(
            user=self.user1.id, username="testuser1", first_name="Test", last_name="User", email="test1@example.com"
        )
        self.user2 = User.objects.create_user(username="testuser2", email="test2@example.com", password="password123")
        self.profile2 = Profile.objects.create(
            user=self.user2.id, username="testuser2", first_name="Other", last_name="User", email="test2@example.com"
        )

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/profile/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser1")

    def test_get_profile_unauthenticated(self):
        response = self.client.get(f"/api/profile/{self.user1.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
