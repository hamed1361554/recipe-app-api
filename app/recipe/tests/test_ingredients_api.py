from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(APITestCase):
    """Test that publicly available ingredients API"""

    def setUp(self):
        """Sets up"""

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(APITestCase):
    """Test that available ingredients API for authorized users"""

    def setUp(self):
        """Sets up"""

        self.user = get_user_model().objects.create_user(
            email='test@sample.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)

    def test_ingredient_list_retrieval(self):
        """Tests that ingredients list retrieves"""

        Ingredient.objects.create(user=self.user, name='kale')
        Ingredient.objects.create(user=self.user, name='salt')

        ings = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ings, many=True)

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_only_ingredients(self):
        """Tests that ingredients list retrieves for login user"""

        other_user = get_user_model().objects.create_user(
                email='othertest@sample.com',
                password='testpass123',
            )

        other_ing = Ingredient.objects.create(user=other_user, name='vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='tumeric')

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0].get('name'), ingredient.name)
        self.assertNotEqual(res.data[0].get('name'), other_ing.name)

    def test_create_ingredient_successful(self):
        """Test new ingredient creation"""

        payload = {'name': 'cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test new invalid ingredient creation fails"""

        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
