from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from profile_user_app.models import Profile
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/authentication/registration/"
        self.user_data = {
            "username": "testuser",
            "first_name": "Max",
            "last_name": "Muster",
            "email": "test@example.com",
            "password": "securepass123",
            "repeated_password": "securepass123"
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_registration_password_mismatch(self):
        self.user_data["repeated_password"] = "wrongpassword"
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_registration_existing_email(self):
        User.objects.create_user(username="existinguser", email=self.user_data["email"], password="test1234")
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

class ActivateAccountViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepass123", is_active=False)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = f"/api/authentication/activate/{self.uidb64}/{self.token}/"

    def test_activate_account_success(self):
        response = self.client.get(self.url)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(self.user.is_active)

    def test_activate_account_invalid_token(self):
        response = self.client.get(f"/api/authentication/activate/{self.uidb64}/wrongtoken/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepass123")
        self.profile = Profile.objects.create(
            user=self.user.id,
            username="testuser",
            first_name="Max",
            last_name="Muster",
            email=self.user.email
        )
        self.url = "/api/authentication/password_reset/"

    def test_request_password_reset_success(self):
        response = self.client.post(self.url, {"email_or_username": "test@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_request_password_reset_invalid_user(self):
        response = self.client.post(self.url, {"email_or_username": "unknown@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepass123")
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = f"/api/authentication/password_reset_confirm/{self.uidb64}/{self.token}/"

    def test_confirm_password_reset_success(self):
        data = {"password": "newsecurepass", "repeated_password": "newsecurepass"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepass"))

    def test_confirm_password_reset_invalid_token(self):
        data = {"password": "newsecurepass", "repeated_password": "newsecurepass"}
        response = self.client.post(f"/api/authentication/password_reset_confirm/{self.uidb64}/wrongtoken/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OldPasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="oldpassword123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = "/api/authentication/old_password_reset/"

    def test_old_password_reset_success(self):
        data = {"old_password": "oldpassword123", "password": "newsecurepass", "repeated_password": "newsecurepass"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepass"))

    def test_old_password_reset_wrong_old_password(self):
        data = {"old_password": "wrongpassword", "password": "newsecurepass", "repeated_password": "newsecurepass"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_old_password_reset_mismatched_new_passwords(self):
        data = {"old_password": "oldpassword123", "password": "newsecurepass", "repeated_password": "mismatchpass"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
