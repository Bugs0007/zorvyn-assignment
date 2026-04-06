from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient

from apps.test_base import BaseAPITestCase


class UserAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("user-list")

    def test_admin_can_list_users(self):
        response = self.admin_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_analyst_cannot_access_users_endpoint(self):
        response = self.analyst_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_access_users_endpoint(self):
        response = self.viewer_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access_users_endpoint(self):
        response = self.unauthenticated_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_endpoint_returns_token_for_valid_credentials(self):
        response = self.unauthenticated_client.post(
            reverse("login"),
            {"username": "admin", "password": "admin123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "admin")

    def test_admin_created_user_password_is_hashed(self):
        response = self.admin_client.post(
            self.list_url,
            {
                "username": "new_user",
                "password": "strongpass123",
                "email": "new@example.com",
                "role": "VIEWER",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = self.admin.__class__.objects.get(username="new_user")
        self.assertNotEqual(created_user.password, "strongpass123")
        self.assertTrue(created_user.check_password("strongpass123"))

    def test_admin_updated_user_password_is_hashed(self):
        response = self.admin_client.patch(
            reverse("user-detail", args=[self.viewer.id]),
            {"password": "updatedpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.viewer.refresh_from_db()
        self.assertNotEqual(self.viewer.password, "updatedpass123")
        self.assertTrue(self.viewer.check_password("updatedpass123"))

    def test_bearer_token_authentication_works_for_protected_endpoint(self):
        token = Token.objects.create(user=self.admin)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.key}")

        response = client.get(reverse("user-me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "admin")
