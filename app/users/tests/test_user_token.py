from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient
import rest_framework.status as status


TOKEN_URL = reverse('users:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserTokenTests(TestCase):
    """User Token Tests"""

    def setUp(self):
        """Sets up"""

        self.client = APIClient()

    def test_create_user_token(self):
        """Tests that user token created successfully"""

        payload = {
            'email': 'test@tosan.com',
            'password': 'testpassword123'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_invalid_user_credentials(self):
        """Tests that invalid user credentials fails"""

        payload = {
            'email': 'test@tosan.com',
            'password': 'testpassword123'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, {**payload, 'password': 'wrongpassword'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_invalid_user(self):
        """Tests that invalid user fails"""

        payload = {
            'email': 'test@tosan.com',
            'password': 'testpassword123'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_invalid_user_password(self):
        """Tests that invalid user fails"""

        payload = {
            'email': 'test@tosan.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
