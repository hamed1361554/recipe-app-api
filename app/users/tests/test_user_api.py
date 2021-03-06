from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

import rest_framework.status as status
from rest_framework.test import APIClient, APITestCase


CREATE_USERS_URL = reverse('users:create')
SELF_USER_URL = reverse('users:me')


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

    def test_unauthorized_user_retrieval(self):
        """Tests that user retrieval needs authorization"""
        res = self.client.post(SELF_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(APITestCase):
    """Private User Api Tests"""

    def setUp(self):
        """Sets up"""

        self.user = get_user_model().objects.create_user(
            email='test@tosan.com',
            password='testpassword',
            name='testuser'
        )

        self.client.force_authenticate(user=self.user)

    def test_authorized_user_retrieval(self):
        """Tests that user retrieval needs authorization"""

        res = self.client.get(SELF_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'id': res.data.get('id'),
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_self_user_invalid_data(self):
        """Tests than null payload is invalid"""

        res = self.client.post(SELF_USER_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update_successful(self):
        """Tests that user update is successful"""

        payload = {'name': 'new name', 'password': 'newpassworduser'}
        res = self.client.patch(SELF_USER_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.user.email)
        self.assertTrue(self.user.check_password(payload['password']))
