from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from login_app.api.serializers import CustomLoginSerializer
from profile_user_app.models import Profile

class CustomLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="securepassword")
        self.profile = Profile.objects.create(
            user=self.user.pk,
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com"
        )

    def test_valid_login_with_email(self):
        serializer = CustomLoginSerializer(data={"username_or_email": "testuser@example.com", "password": "securepassword"})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_valid_login_with_username(self):
        serializer = CustomLoginSerializer(data={"username_or_email": "testuser", "password": "securepassword"})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_invalid_login(self):
        serializer = CustomLoginSerializer(data={"username_or_email": "testuser@example.com", "password": "wrongpassword"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("detail", serializer.errors)

class CostomLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="securepassword")
        self.profile = Profile.objects.create(
            user=self.user.id,
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com"
        )
        self.token = Token.objects.create(user=self.user)

    def test_successful_login(self):
        response = self.client.post("/api/login/", {"username_or_email": "testuser@example.com", "password": "securepassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["username"], "testuser")

    def test_login_with_wrong_credentials(self):
        response = self.client.post("/api/videos/", {"username_or_email": "testuser@example.com", "password": "wrongpassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_login_with_deactivated_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post("/api/videos/", {"username_or_email": "testuser@example.com", "password": "securepassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

