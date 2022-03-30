from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(APITestCase):
    """Public Tags Api Test"""

    def test_unauthorized_access_failed(self):
        """Tests that unauthorized access would fail"""

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(APITestCase):
    """Private Tags Api Test"""

    def setUp(self):
        """Sets up"""

        self.user = get_user_model().objects.create_user(
            email='test@sample.com',
            password='testpassword123456',
            name='testuser')
        self.client.force_authenticate(user=self.user)

    def test_tags_retrieval(self):
        """Tests that tags retrieval is successful"""

        Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='desert')

        res = self.client.get(TAGS_URL)
        serializer = TagSerializer(Tag.objects.all().order_by('-name'), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tests that tags limited to their user"""

        other_user = get_user_model().objects.create_user(
            email='other@sample.com',
            password='whatsoeveritwouldbe',
            name='otherone'
        )
        other_tag = Tag.objects.create(user=other_user,
                                       name='flaky')

        tag = Tag.objects.create(user=self.user,
                                 name='meatloaf')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0].get('name'), tag.name)
        self.assertNotEqual(res.data[0].get('name'), other_tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
