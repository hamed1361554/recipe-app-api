from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import rest_framework.status as status


class AdminSiteTests(TestCase):
    """Admin Site Tests"""
    
    def setUp(self):
        """Sets up admint site tests."""
        
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fake.com',
            password='drowssap'
        )
        self.client.force_login(self.admin_user)
        
        self.user = get_user_model().objects.create_user(
            email='user@fake.com',
            password='123456',
            name='test user name'
        )
        
    def test_user_listed(self):
        """Tests that created users listed"""
        
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.admin_user.email)
    
    def test_user_changed(self):
        """Tests that users changed"""
        
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        
        self.assertTrue(status.is_success(res.status_code))

    def test_user_created(self):
        """Tests that user created"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertTrue(status.is_success(res.status_code))
