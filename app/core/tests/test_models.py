from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    Model Tests
    """
    
    def test_create_user_with_email_successful(self):
        """Tests successfully creating user with email"""
        
        email = 'test@outlook.com'
        password = 'TestPassword123456'
        
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_normalized_email_user_creation(self):
        """Test user creation by normalized email"""
        
        email = 'test@HOTMAIL.com'
        user = get_user_model().objects.create_user(email=email,
                                                    password='123')
        
        self.assertEqual(user.email, email.lower())
    
    def test_null_email_user_creation(self):
        """Tests null email results in value error"""
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password='test')
    
    def test_create_super_user(self):
        """Test super user createion"""
        
        user = get_user_model().objects.create_superuser(
            email='superuser@google.com',
            password='test123')
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
