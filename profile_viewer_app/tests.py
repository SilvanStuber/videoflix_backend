from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from profile_viewer_app.models import ProfileViewer
from profile_viewer_app.api.serializers import ProfileViewerSerializer
from profile_viewer_app.api.permissions import IsOwnerOrAdmin, IsOwnerFromViewerOrAdmin

class ProfileViewerModelTest(TestCase):
    def setUp(self):
        self.viewer = ProfileViewer.objects.create(
            user=1,
            viewer_id=None,
            viewername="Test Viewer",
            picture_file="test.jpg"
        )

    def test_profile_viewer_creation(self):
        self.assertEqual(self.viewer.viewername, "Test Viewer")

class ProfileViewerSerializerTest(TestCase):
    def setUp(self):
        self.viewer = ProfileViewer.objects.create(
            user=1,
            viewer_id=None,
            viewername="Test Viewer",
            picture_file="test.jpg"
        )
        self.serializer = ProfileViewerSerializer(instance=self.viewer)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"user", "viewer_id", "viewername", "picture_file"})

class ProfileViewerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.client.force_authenticate(user=self.user)
        self.viewer = ProfileViewer.objects.create(
            user=self.user.id,
            viewer_id=None,
            viewername="Test Viewer",
            picture_file="test.jpg"
        )

    def test_get_profile_viewers(self):
        response = self.client.get("/api/viewer/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile_viewer(self):
        data = {
            "user": self.user.id,
            "viewername": "Neuer Viewer",
            "picture_file": "bild.png"
        }
        response = self.client.post("/api/viewer/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_profile_viewer(self):
        response = self.client.get(f"/api/viewer/{self.viewer.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_viewer(self):
        data = {"viewername": "Bearbeiteter Name", "user": self.user.id}
        response = self.client.patch(f"/api/viewer/{self.viewer.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_profile_viewer(self):
        response = self.client.delete(f"/api/viewer/{self.viewer.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProfileViewerPermissionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.viewer = ProfileViewer.objects.create(
            user=self.user.id,
            viewer_id=None,
            viewername="Test Viewer",
            picture_file="test.jpg"
        )
        self.factory = APIRequestFactory()

    def test_is_owner_or_admin(self):
        request = self.factory.get(f"/api/viewer/{self.viewer.pk}/")
        request.user = self.user
        view = lambda: None
        setattr(view, "kwargs", {"pk": self.viewer.pk})
        perm = IsOwnerOrAdmin()
        self.assertTrue(perm.has_object_permission(request, view, self.viewer))

    def test_is_owner_from_viewer_or_admin(self):
        other_user = User.objects.create_user(username="otheruser", password="password123")
        request = self.factory.get(f"/api/viewer/{self.viewer.pk}/")
        request.user = other_user
        view = lambda: None
        setattr(view, "kwargs", {"pk": self.viewer.pk})
        perm = IsOwnerFromViewerOrAdmin()
        self.assertFalse(perm.has_object_permission(request, view, self.viewer))


