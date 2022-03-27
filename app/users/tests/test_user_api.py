from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

import rest_framework.status as status
from rest_framework.test import APIClient


CREATE_USERS_URL = reverse('users:create')


class PublicUserApiTests(TestCase):
    """Public User Api Tests"""

    def setUp(self):
        """Sets up"""

        self.client = APIClient()

    def test_create_user_successfully(self):
        """Tests that user successfully created."""

        payload = {
            "email": "test@tosan.com",
            "password": "testpass",
            "name": "test user"
        }
        res = self.client.post(CREATE_USERS_URL, payload)

        user = get_user_model().objects.get(**res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], user.email)
        self.assertTrue(user.check_password(payload['password']))
        self.assertIn('id', res.data)
        self.assertNotIn('password', res.data)

    def test_user_creation_duplication_error(self):
        """Tests that user already created"""

        payload = {
            "email": "test@tosan.com",
            "password": "testpass",
            "name": "test user"
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(CREATE_USERS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_valid_password(self):
        """Tests that invalid password fails at creation"""

        payload = {
            "email": "test@tosan.com",
            "password": "pw",
        }
        res = self.client.post(CREATE_USERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(email=payload['email']).exists())
